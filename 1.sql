WITH get_data AS (
SELECT b.client_number, e.outcome, COUNT(*) as cnt
FROM bid b
LEFT JOIN event_value e ON b.play_id = e.play_id
WHERE b.coefficient = e.value
GROUP BY 1, 2
)
SELECT t1.client_number, t1.cnt as win, t2.cnt as lose
FROM get_data t1
LEFT JOIN get_data t2 ON t1.client_number = t2.client_number
WHERE t1.outcome = 'win' and t2.outcome = 'lose'
ORDER BY 1 ASC
