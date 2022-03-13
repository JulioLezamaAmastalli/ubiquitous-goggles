import pandas as pd
import mysql.connector
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

client = mysql.connector.connect(**config['connection'])
cursor = client.cursor()

#### Create DB and Tables

with open('create_h2h_db.sql') as ddl:
    cursor.execute(ddl.read())

with open('create_h2h_general.sql') as ddl:
    cursor.execute(ddl.read())

with open('create_h2h_scores.sql') as ddl:
    cursor.execute(ddl.read())

df_general = df.copy().drop(dropped_columns + to_other_tables, 1)

df_scores = pd.DataFrame(columns = ['id', 'localteam_score', 'visitorteam_score', 'localteam_pen_score',
                                    'visitorteam_pen_score', 'ht_score', 'ft_score', 'et_score', 'ps_score'])
for k in range(df.shape[0]):
    temp = pd.DataFrame({key:[value] for key,value in df['scores'].iloc[k].items()})
    temp['id'] = df.iloc[k]['id']
    df_scores = pd.concat([df_scores, temp])

def list_of_tuples(df):
    
    all_values = []
    
    for k in range(df.shape[0]):
        temp = df.iloc[k]
        temp = temp.astype(str)
        temp = tuple(temp)
        all_values.append(temp)
        
    return all_values

general_values = list_of_tuples(df_general)
scores_values = list_of_tuples(df_scores)

for value in general_values:
    with open('insert_h2h_general.sql') as dml:
        try:
            cursor.execute(dml.read(), value)
            dml.close()
        except mysql.connector.IntegrityError as err:
            print("Something went wrong: {}".format(err))
            dml.close()
            pass

for value in scores_values:
    with open('insert_h2h_scores.sql') as dml:
        try:
            cursor.execute(dml.read(), value)
            dml.close()
        except mysql.connector.IntegrityError as err:
            print("Something went wrong: {}".format(err))
            dml.close()
            pass

client.commit()