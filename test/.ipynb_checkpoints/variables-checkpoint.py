# +
############################## Variables ##############################

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


############################## Functions ##############################

def head2head(id1, id2):
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
    head2head_url = f"head2head/{id1}/{id2}"
    end_url = f"?api_token={sports_key}&include="
    url = base_url + head2head_url + end_url
    
    ### Request 
    r = requests.get(url)
    
    return r.json()['data']
