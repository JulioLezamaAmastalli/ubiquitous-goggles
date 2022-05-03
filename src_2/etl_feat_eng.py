########
# LOAD DATA FROM SQL
########
import pandas as pd
import yaml

### User defined
import variables_n_functions as vnf

config_file = open('config.yaml', 'r')
config = yaml.safe_load(config_file)
import mysql.connector

client = mysql.connector.connect(**config['connection'])
cursor = client.cursor()

df=pd.read_sql('SELECT * FROM h2h.source', con=client)

##########
# GENERAL DATA FEAT ENG
#########

### Define columns to drop or that will be added to other tables
dropped_columns = ['details']
to_other_tables = ['weather_report', 'formations', 'scores', 'time_data', 'coaches', 'standings', 'assistants', 'colors']


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

##########
# SCORES FEAT ENG
#########

df_scores = pd.DataFrame(columns = ['id', 'localteam_score', 'visitorteam_score', 'localteam_pen_score',
                                    'visitorteam_pen_score', 'ht_score', 'ft_score', 'et_score', 'ps_score'])
for k in range(df.shape[0]):
    temp = pd.DataFrame({key:[value] for key,value in eval(df['scores'].iloc[k]).items()})
#    temp = pd.DataFrame({key:[value] for key,value in df['scores'].iloc[k].items()})
    temp['id'] = df.iloc[k]['id']
    df_scores = pd.concat([df_scores, temp])
    

# en esta parte no estamos haciendo mucho solo acomodando la tabla final
#############################
#DATA ENGERINING
#############################
frames = [df_general.set_index("id"),df_scores.set_index("id"),df_standings.set_index("id")]
model_data = pd.concat(frames,axis=1)


import numpy as np
# Create Y variable: 1 if local wins, 0 in any other case
model_data['Y'] = np.where(model_data['winner_team_id']==model_data['localteam_id'], 1, 0)

# Filter only columns for model
model_data=model_data[["Y","league_id","season_id","venue_id","referee_id","localteam_id",'visitorteam_id',"localteam_position","visitorteam_position","match_day"]]
#frames = [df_general["id"], model_data]
#model_data = pd.concat(frames,axis=1)
model_data.reset_index(inplace=True)
 
#############################
## DROP TO SQL TABLE
#############################

#### Create DB and Tables

with open("sql/create_h2h_model.sql") as ddl:
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
    with open("sql/insert_h2h_model.sql") as dml:
        try:
            cursor.execute(dml.read(), value)
            dml.close()
        except mysql.connector.IntegrityError as err:
            print("Something went wrong: {}".format(err))
            dml.close()
            pass

client.commit()
