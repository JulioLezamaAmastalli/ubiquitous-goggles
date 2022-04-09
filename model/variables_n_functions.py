import requests
import pandas as pd

# ############################# Variables ##############################

columnas_df = [
               'id',
               'league_id',
               'season_id',
               'stage_id',
               'round_id',
               'group_id',
               'aggregate_id',
               'venue_id',
               'referee_id',
               'localteam_id',
               'visitorteam_id',
               'winner_team_id',
               'weather_report',
               'commentaries',
               'attendance',
               'pitch',
               'details',
               'neutral_venue',
               'winning_odds_calculated',
               'formations',
               'scores',
               'time',
               'coaches',
               'standings',
               'assistants',
               'leg',
               'colors',
               'deleted',
               'is_placeholder'
              ]


# ############################# Functions ##############################

### IMPORTANTE!!! HAY QUE AniADIR LA VENTANA DE TIEMPO
### COMO PARAMETRO
def head2head(id1, id2, sports_key):
    """
    Return the historical match results and characteristics between any 2 given teams

    Input :
        id1 : int; id for the first team
        id2 : int; id for the second team

    Output :
        list containing dictionaries with the characteristics of every match

    """
    
    ### Define the URL
    base_url = "https://soccer.sportmonks.com/api/v2.0/"
    head2head_url = "head2head/" + str(id1) + "/" + str(id2)
    end_url = "?api_token=" + str(sports_key) + "&include="
    url = base_url + head2head_url + end_url
    
    ### Request 
    r = requests.get(url)
    
    return r.json()['data']

def booleanize(x):
    """
    Convert True to 1, False to 0, else to -1
    """
    if x == True:
        return 1
    elif x == False:
        return 0
    else:
        return -1

def expand_dictionary(col, df):
    
    aux_df = pd.DataFrame(columns = df[col].iloc[0].keys())
    
    for k in range(len(df)):
        aux = pd.DataFrame(df[col].iloc[k].values()).transpose()
        aux.columns = df[col].iloc[k].keys()
        aux_df = pd.concat([aux_df, aux])
        
    return aux_df

def make_other_category(col, df, c, replace):

    aux = df[col].value_counts()
    less_than_c = list(aux[aux < c].index)
    
    return df[col].apply(lambda x : replace if x in less_than_c else x)