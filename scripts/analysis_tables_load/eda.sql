SELECT * FROM staging.segments WHERE JSON_EXTRACT_SCALAR(map, '$.id') = 's1386542'
SELECT * FROM analysis.segments WHERE segment_id = 's4331288'
SELECT COUNT(*), segment_id FROM analysis.segments GROUP BY segment_id ORDER BY 1 DESC;

SELECT ROW_NUMBER() OVER() AS surrogate_key,
    stg_s.*
FROM staging.segments stg_s
LEFT JOIN analysis.segments an_s
    ON stg_s.name = an_s.name
    AND stg_s.activity_type = an_s.activity_type
    AND stg_s.distance = an_s.distance
WHERE an_s.name IS NULL;

SELECT map FROM staging.segments LIMIT 1;

SELECT * FROM staging.segments WHERE JSON_EXTRACT_SCALAR(map, '$.id') = 's10149879';

DELETE FROM analysis.segments WHERE 1 = 1;


UPDATE staging.segments SET insert_date = CURRENT_DATETIME() WHERE insert_date IS NULL;
UPDATE staging.leaderboard SET insert_date = CURRENT_DATETIME() WHERE insert_date IS NULL;

SELECT * FROM analysis.segments;

SELECT *
FROM staging.lea