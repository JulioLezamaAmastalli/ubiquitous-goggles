CREATE TABLE IF NOT EXISTS h2h.general (
    id VARCHAR(12), 
    league_id VARCHAR(12), 
    season_id VARCHAR(12), 
    stage_id VARCHAR(12), 
    round_id VARCHAR(12), 
    group_id VARCHAR(12),
    aggregate_id VARCHAR(12), 
    venue_id VARCHAR(12), 
    referee_id VARCHAR(12), 
    localteam_id VARCHAR(12),
    visitorteam_id VARCHAR(12),
    winner_team_id VARCHAR(12),
    -- commentaries VARCHAR(5),
    commentaries TINYINT(1),
    -- attendance VARCHAR(7),
    attendance NUMERIC(10, 0),
    pitch VARCHAR(30),
    -- neutral_venue VARCHAR(5),
    neutral_venue TINYINT(1),
    -- winning_odds_calculated VARCHAR(5),
    winning_odds_calculated TINYINT(1),
    leg VARCHAR(10),
    -- deleted VARCHAR(5),
    deleted TINYINT(1),
    -- is_placeholder VARCHAR(5),
    is_placeholder TINYINT(1),
    UNIQUE KEY  (`id`)
);