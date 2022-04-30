INSERT INTO h2h.scores (
  id,
  localteam_score,
  visitorteam_score,
  localteam_pen_score,
  visitorteam_pen_score,
  ht_score,
  ft_score,
  et_score,
  ps_score
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