import pandas as pd
import yaml

### User defined
import variables_n_functions as vnf

config_file = open('config.yaml', 'r')
config = yaml.safe_load(config_file)

teams = config['teams']

### We initialize the df with the appropriate column names
df = pd.DataFrame(columns = vnf.columnas_df)

### The following variable is auxiliar to avoid duplicate requests
teams_aux = list(teams.keys())

### We recover the match history between every unique team - team combination, and store it in the df
for team_1 in teams.keys():
    teams_aux.remove(team_1)
    for team_2 in teams_aux:
        h2h = vnf.head2head(team_1, team_2, config['sports_token'])
        df = pd.concat([df] + [pd.DataFrame(pd.Series(h2h[k])).transpose() for k in range(len(h2h))])        

### Define columns to drop or that will be added to other tables
dropped_columns = ['details']
to_other_tables = ['weather_report', 'formations', 'scores', 'time', 'coaches', 'standings', 'assistants', 'colors']

config_file = open('config.yaml', 'r')
config = yaml.safe_load(config_file)


import mysql.connector

client = mysql.connector.connect(**config['connection'])
cursor = client.cursor()

#### Create DB and Tables

with open('sql/create_h2h_db.sql') as ddl:
    cursor.execute(ddl.read())

with open('sql/create_h2h_standings.sql') as ddl:
    cursor.execute(ddl.read())
    
    
df_standings = pd.DataFrame(columns = ['id'])

for k in range(df.shape[0]):
#     temp = pd.DataFrame({key:[value] for key,value in eval(df['scores'].iloc[k]).items()})
    temp = pd.DataFrame({key:[value] for key,value in df['standings'].iloc[k].items()})
    temp['id'] = df.iloc[k]['id']
    df_standings = pd.concat([df_standings, temp])

#################### Transformations ####################
  
###### h2h.standings

df_standings['id'] = df_standings['id']
df_standings['localteam_position'] = df_standings['localteam_position'].fillna(-1)# Integer
df_standings['visitorteam_position'] = df_standings['visitorteam_position'].fillna(-1)# Integer

def list_of_tuples(df):
    
    all_values = []
    
    for k in range(df.shape[0]):
        temp = df.iloc[k]
        temp = temp.astype(str)
        temp = tuple(temp)
        all_values.append(temp)
        
    return all_values

standings_values = list_of_tuples(df_standings)

for value in standings_values:
    with open('sql/insert_h2h_standings.sql') as dml:
        try:
            cursor.execute(dml.read(), value)
            dml.close()
        except mysql.connector.IntegrityError as err:
            print("Something went wrong: {}".format(err))
            dml.close()
            pass

client.commit()