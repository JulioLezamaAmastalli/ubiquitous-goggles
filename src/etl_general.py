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

with open('sql/create_h2h_general.sql') as ddl:
    cursor.execute(ddl.read())


df_general = df.copy().drop(dropped_columns + to_other_tables, 1)


#################### Transformations ####################
    
###### h2h.general

### ID variables
df_general['id'] = df_general['id']
df_general['league_id'] = df_general['league_id'].fillna(-1)
df_general['season_id'] = df_general['season_id'].fillna(-1)
df_general['stage_id'] = df_general['stage_id'].fillna(-1)
df_general['round_id'] = df_general['round_id'].fillna(-1)
df_general['group_id'] = df_general['group_id'].fillna(-1)
df_general['aggregate_id'] = df_general['aggregate_id'].fillna(-1)
df_general['venue_id'] = df_general['venue_id'].fillna(-1)
df_general['referee_id'] = df_general['referee_id'].fillna(-1)
df_general['localteam_id'] = df_general['localteam_id'].fillna(-1)
df_general['visitorteam_id'] = df_general['visitorteam_id'].fillna(-1)
df_general['winner_team_id'] = df_general['winner_team_id'].fillna(-1)

### Other variables
df_general['commentaries'] = df_general['commentaries'].apply(vnf.booleanize)# Boolean
df_general['attendance'] = df_general['attendance'].fillna(-1)# Integer
df_general['pitch'] = df_general['pitch'].apply(lambda x: "None" if x is None else x) # Categorical
df_general['neutral_venue'] = df_general['neutral_venue'].apply(vnf.booleanize)# Boolean
df_general['winning_odds_calculated'] = df_general['winning_odds_calculated'].apply(vnf.booleanize)# Boolean
df_general['deleted'] = df_general['deleted'].apply(vnf.booleanize)# Boolean
df_general['is_placeholder'] = df_general['is_placeholder'].apply(vnf.booleanize)# Boolean
df_general['leg'] = df_general['leg'].fillna(-1)


def list_of_tuples(df):
    
    all_values = []
    
    for k in range(df.shape[0]):
        temp = df.iloc[k]
        temp = temp.astype(str)
        temp = tuple(temp)
        all_values.append(temp)
        
    return all_values

general_values = list_of_tuples(df_general)


for value in general_values:
    with open('sql/insert_h2h_general.sql') as dml:
        try:
            cursor.execute(dml.read(), value)
            dml.close()
        except mysql.connector.IntegrityError as err:
            print("Something went wrong: {}".format(err))
            dml.close()
            pass

client.commit()