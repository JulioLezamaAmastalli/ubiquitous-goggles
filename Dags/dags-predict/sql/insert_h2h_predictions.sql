INSERT IGNORE INTO h2h.predictions (
    id,
    league_id, 
    season_id, 
    venue_id, 
    referee_id, 
    localteam_id,
    visitorteam_id,
    localteam_position, 
    visitorteam_position
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
  %s
)