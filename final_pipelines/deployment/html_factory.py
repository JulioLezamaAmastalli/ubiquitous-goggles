
###############################################
## DEFINE DIRECTORIES AND PATHS FOR AIRFLOW
############################################### 
import variables_n_functions as vnf


###############################################
## CONNECTION WITH DB
###############################################                      
import pandas as pd
import yaml
import mysql.connector

config_file = open('config.yaml', 'r')
config = yaml.safe_load(config_file)

client = mysql.connector.connect(**config['connection'])
cursor = client.cursor()


###############################################
## DATA REQUEST TO DB: MATCHES FROM NEXT WEEK 7 DAYS
############################################### 

### DATES
from datetime import date, timedelta
import numpy as np


end = date.today()
start = end - timedelta(7)

end = end.strftime("%Y-%m-%d")
start = start.strftime("%Y-%m-%d")

between = '"'+start+'"' + ' and ' + '"'+end+'"'
data_request_string='SELECT * FROM h2h.model2 WHERE (match_day BETWEEN ' +between+ ')'
df=pd.read_sql(data_request_string, con=client)

###############################################
## CREATE OUTPUT DATAFRAME OF PREDICtiONS
############################################### 

catalogue=pd.read_csv("teams_flags.csv")

####
#Formato para el merge
catalogue['team']=catalogue['team'].astype('int64')
df['localteam_id']=df['localteam_id'].astype('int64')
df['visitorteam_id']=df['visitorteam_id'].astype('int64')

####
#MERGE
df=pd.merge(df, catalogue, left_on='localteam_id', right_on='team')
df=pd.merge(df, catalogue, left_on='visitorteam_id', right_on='team')
df
# COLNAMES
df.columns = ['id', 'Y', 'league_id', 'season_id', 'venue_id', 'referee_id',
       'localteam_id', 'visitorteam_id', 'localteam_position',
      'visitorteam_position', 'match_day',"x","x2","localteam_flag",
        "localteam_name","x3","x4","visitorteam_flag","visitorteam_name"]

######## CREO EL DATAFRAME QUE VOY A MOSTRAR ######
output= df[['Y','localteam_flag','localteam_name','visitorteam_flag','visitorteam_name','match_day']]

####### CREO EL HTML ######
from IPython.core.display import HTML
def path_to_image_html(path):
    return '<img src="'+ path + '" width="60" >'
output.to_html('index.html',escape=False, formatters=dict(localteam_flag=path_to_image_html, visitorteam_flag=path_to_image_html))
