import os
### directories
path = os.path.dirname(os.path.abspath(__file__))
script_path_yaml=os.path.join(path, 'config.yaml')
sql_create_predictons=os.path.join(path, 'sql/create_h2h_predictions.sql')
sql_insert_predictions=os.path.join(path, 'sql/insert_h2h_predictions.sql')
to_predict_data = os.path.join(path,  'features.txt')


#############################
#READ DATA to predict from text
#############################

import pandas as pd
to_predict = pd.read_csv(to_predict_data, sep="\t")



#############################
#READ DATAFROM MYSQL
#############################
import mysql.connector
import yaml
import pandas as pd
config_file = open(script_path_yaml, 'r')
config = yaml.safe_load(config_file)
con = mysql.connector.connect(**config['connection'])


#############################
## DROP TO SQL TABLE
#############################

client = mysql.connector.connect(**config['connection'])
cursor = client.cursor()

#### Create DB and Tables

with open(sql_create_predictons) as ddl:
    cursor.execute(ddl.read())

def list_of_tuples(df):
    
    all_values = []
    
    for k in range(df.shape[0]):
        temp = df.iloc[k]
        temp = temp.astype(str)
        temp = tuple(temp)
        all_values.append(temp)
        
    return all_values

to_predict_values = list_of_tuples(to_predict)


for value in to_predict_values:
    with open(sql_insert_predictions) as dml:
        try:
            cursor.execute(dml.read(), value)
            dml.close()
        except mysql.connector.IntegrityError as err:
            print("Something went wrong: {}".format(err))
            dml.close()
            pass

client.commit()