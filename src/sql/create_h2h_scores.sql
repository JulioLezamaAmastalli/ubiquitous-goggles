CREATE TABLE IF NOT EXISTS h2h.scores (
    id VARCHAR(12), 
    localteam_score NUMERIC(2, 0),
    visitorteam_score NUMERIC(2, 0),
    localteam_pen_score VARCHAR(4),
    visitorteam_pen_score VARCHAR(4),
    ht_score VARCHAR(5),
    ft_score VARCHAR(5),
    et_score VARCHAR(5),
    ps_score VARCHAR(5),
    UNIQUE KEY  (`id`)
);