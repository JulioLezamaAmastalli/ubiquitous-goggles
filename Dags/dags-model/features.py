
import os
### directories
path = os.path.dirname(os.path.abspath(__file__))
script_path_yaml=os.path.join(path, 'config.yaml')
sql_create_model_table=os.path.join(path, 'sql/create_h2h_model.sql')
sql_insert_model_table=os.path.join(path, 'sql/insert_h2h_model.sql')




#############################
#READ DATAFROM MYSQL
#############################
import mysql.connector
import yaml
import pandas as pd
config_file = open(script_path_yaml, 'r')
config = yaml.safe_load(config_file)
con = mysql.connector.connect(**config['connection'])

### PD dataframes

general = pd.read_sql('SELECT * FROM general', con=con)
scores = pd.read_sql('SELECT * FROM scores', con=con)
standings = pd.read_sql('SELECT * FROM standings', con=con)

#############################
#DATA ENGERINING
#############################
frames = [general, scores, standings]
model_data = pd.concat(frames,axis=1)


import numpy as np
# Create Y variable: 1 if local wins, 0 in any other case
model_data['Y'] = np.where(model_data['winner_team_id']==model_data['localteam_id'], 1, 0)

# Filter only columns for model
model_data=model_data[["Y","league_id","season_id","venue_id","referee_id","localteam_id",'visitorteam_id',"localteam_position","visitorteam_position"]]
frames = [general["id"], model_data]
model_data = pd.concat(frames,axis=1)

#############################
## DROP TO SQL TABLE
#############################

client = mysql.connector.connect(**config['connection'])
cursor = client.cursor()

#### Create DB and Tables

with open(sql_create_model_table) as ddl:
    cursor.execute(ddl.read())

def list_of_tuples(df):
    
    all_values = []
    
    for k in range(df.shape[0]):
        temp = df.iloc[k]
        temp = temp.astype(str)
        temp = tuple(temp)
        all_values.append(temp)
        
    return all_values

model_values = list_of_tuples(model_data)


for value in model_values:
    with open(sql_insert_model_table) as dml:
        try:
            cursor.execute(dml.read(), value)
            dml.close()
        except mysql.connector.IntegrityError as err:
            print("Something went wrong: {}".format(err))
            dml.close()
            pass

client.commit()
    