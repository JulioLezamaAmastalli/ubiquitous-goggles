CREATE TABLE IF NOT EXISTS h2h.prediction (
    id VARCHAR(12), 
    league_id VARCHAR(12), 
    season_id VARCHAR(12), 
    venue_id VARCHAR(12), 
    referee_id VARCHAR(12), 
    localteam_id VARCHAR(12),
    visitorteam_id VARCHAR(12),
    localteam_position numeric(2, 0), 
    visitorteam_position numeric(2, 0),
    probs VARCHAR(60),
    UNIQUE KEY  (`id`)
);
