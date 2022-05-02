INSERT IGNORE INTO h2h.prediction (
    id,
    league_id, 
    season_id, 
    venue_id, 
    referee_id, 
    localteam_id,
    visitorteam_id,
    localteam_position, 
    visitorteam_position,
    probs
)

VALUES (
  %s,
  %s,
  %s,
  %s,
  %s,  
  %s,
  %s,
  %s,
  %s,
  %s
)