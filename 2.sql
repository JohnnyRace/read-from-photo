WITH distinct_res AS (
SELECT home_team, away_team, COUNT(*) AS cnt
FROM event_entity
GROUP BY 1, 2
),
joined_teams AS (
SELECT t1.home_team as t1_home_team, t1.away_team as t1_away_team, t1.cnt as t1_cnt, t2.home_team as t2_home_team, t2.away_team as t2_away_team, t2.cnt as t2_cnt
FROM distinct_res t1
LEFT JOIN distinct_res t2 ON t1.home_team = t2.away_team AND t2.home_team = t1.away_team 
),
union_data AS (
SELECT t1_home_team, t1_away_team, t1_cnt
FROM joined_teams
UNION ALL
SELECT t2_away_team, t2_home_team, t1_cnt
FROM joined_teams
)
SELECT t1_home_team, t1_away_team, SUM(t1_cnt)
FROM union_data
WHERE t1_home_team IS NOT NULL AND t1_away_team IS NOT NULL 
GROUP BY 1, 2
ORDER BY 3 ASC 
