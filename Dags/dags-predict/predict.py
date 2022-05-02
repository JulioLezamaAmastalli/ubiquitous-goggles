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

print(results)