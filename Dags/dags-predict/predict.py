### script2.py
import yaml
import pandas as pd
import mysql.connector

import os
### directories
path = os.path.dirname(os.path.abspath(__file__))
yaml_dir=os.path.join(path, 'config.yaml')

### Open config file
config_file = open(yaml_dir, 'r')
config = yaml.safe_load(config_file)

### Connect to the DB
client = mysql.connector.connect(**config['connection'])
cursor = client.cursor()

### Get set of features for which we want to make a prediction
cursor.execute("SELECT * FROM h2h.prediction")
colnames = cursor.column_names
res = cursor.fetchall()
df = pd.DataFrame(columns = colnames)

### Arrange them into a DF
for k in range(len(res)):

    aux = pd.DataFrame(res[k]).transpose()
    aux.columns = colnames
    df = pd.concat([df, aux])
    
df.set_index('id', inplace = True)

# Convert categorical to dummies
X = df[[col for col in df.columns if col != 'probs']]

# Make the predictions
from model_prediction import CustomModelPrediction
classifier = CustomModelPrediction.from_path(path)
results = classifier.predict(X)

# Print the results 
for localteam, visitorteam, result in zip(X['localteam_id'].values, X['visitorteam_id'].values, results):
    print(f'Probability of localteam {localteam} winning vs visitorteam {visitorteam}: ' + str(round(100*result[0], 2)) + '%')

### We will add the predictions bask to the DB. For this, we
### convert the results to a string
to_predict = X.copy()
to_predict['probs'] = results
to_predict['probs'] = to_predict['probs'].apply(lambda x: str(x[0]) + ',' + str(x[1]))

def list_of_tuples(df):
    
    all_values = []
    
    for k in range(df.shape[0]):
        temp = df.copy()
        temp = temp.reset_index()
        temp = temp[['probs', 'id']]
        temp = temp.iloc[k]                        
        temp = temp.astype(str)
        temp = tuple(temp)
        all_values.append(temp)
        
    return all_values

to_predict_values = list_of_tuples(to_predict)

### Since the table already exists, we update the na values
### in it with the probabilities we calculated
sql_com = "UPDATE h2h.prediction SET probs = %s WHERE id = %s"

for value in to_predict_values:
    try:
        cursor.execute(sql_com, value)
    except mysql.connector.IntegrityError as err:
        print("Something went wrong: {}".format(err))        
        pass

client.commit()