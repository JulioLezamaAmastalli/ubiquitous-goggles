CREATE TABLE IF NOT EXISTS h2h.standings (
    id VARCHAR(12), 
    localteam_position NUMERIC(2, 0),
    visitorteam_position NUMERIC(2, 0),
    UNIQUE KEY  (`id`)
);