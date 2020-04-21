"""SQL statements to create analytics tables.

:authors
    JP at 19/04/20
"""

# Join the staging table to the analysis table and insert
# Some segments are retrieved from multiple sections of the grid, the group by ensures that no duplicates are inserted
# GROUP is used rather than DISTINCT as the effort/athlete counts change over time
load_segments = """
INSERT INTO analysis.segments
SELECT JSON_EXTRACT_SCALAR(stg_s.map, '$.id') segment_id,
    stg_s.name,
    stg_s.activity_type,
    stg_s.distance,
    stg_s.average_grade,
    stg_s.maximum_grade,
    stg_s.elevation_high,
    stg_s.elevation_low,
    stg_s.start_latlng,
    stg_s.end_latlng,
    stg_s.start_latitude,
    stg_s.end_latitude,
    stg_s.start_longitude,
    stg_s.end_longitude,
    stg_s.climb_category,
    stg_s.city,
    stg_s.state,
    stg_s.country,
    stg_s.private,
    stg_s.starred,
    stg_s.created_at,
    MAX(stg_s.updated_at),
    stg_s.total_elevation_gain,
    stg_s.map,
    MAX(stg_s.effort_count),
    MAX(stg_s.athlete_count),
    stg_s.hazardous,
    MAX(stg_s.star_count),
    stg_s.pr_time,
    stg_s.starred_date,
    stg_s.athlete_pr_effort
FROM staging.segments stg_s
LEFT JOIN analysis.segments an_s
  ON stg_s.name = an_s.name
  AND stg_s.activity_type = an_s.activity_type
  AND stg_s.distance = an_s.distance
  AND JSON_EXTRACT_SCALAR(stg_s.map, '$.id') = an_s.segment_id
WHERE an_s.segment_id IS NULL
AND stg_s.name IS NOT NULL
GROUP BY stg_s.name,
    stg_s.activity_type,
    stg_s.distance,
    stg_s.average_grade,
    stg_s.maximum_grade,
    stg_s.elevation_high,
    stg_s.elevation_low,
    stg_s.start_latlng,
    stg_s.end_latlng,
    stg_s.start_latitude,
    stg_s.end_latitude,
    stg_s.start_longitude,
    stg_s.end_longitude,
    stg_s.climb_category,
    stg_s.city,
    stg_s.state,
    stg_s.country,
    stg_s.private,
    stg_s.starred,
    stg_s.created_at,
    stg_s.total_elevation_gain,
    stg_s.map,
    stg_s.hazardous,
    stg_s.pr_time,
    stg_s.starred_date,
    stg_s.athlete_pr_effort
"""

load_leaderboard = """
INSERT INTO analysis.leaderboard
SELECT leaderboard_id,
        segment_id,
        elapsed_time,
        TIME_DIFF(elapsed_time, TIME(0,0,0), SECOND) elapsed_time_seconds,
        segment_distance,
        ROUND(segment_distance/TIME_DIFF(elapsed_time, TIME(0,0,0), SECOND),2) speed_ms,
        start_date,
        rank
FROM (
SELECT CONCAT(an_s.segment_id, "_", stg_l.rank) leaderboard_id,
        an_s.segment_id,
        MIN(CAST(stg_l.elapsed_time AS TIME)) elapsed_time,
        stg_l.segment_distance,
        MIN(CAST(stg_l.start_date AS TIMESTAMP)) start_date,
        stg_l.rank
        FROM staging.leaderboard stg_l
        JOIN analysis.segments an_s
            ON stg_l.segment_name = an_s.name
            AND stg_l.segment_distance = an_s.distance
            AND stg_l.segment_start_latlng = an_s.start_latlng
        LEFT JOIN analysis.leaderboard an_l
            ON CONCAT(an_s.segment_id, "_", stg_l.rank) = an_l.leaderboard_id
        WHERE an_l.leaderboard_id IS NULL
        GROUP BY an_s.segment_id,
        stg_l.rank,
        stg_l.segment_distance)
"""



load_queries = [(load_segments, 'analysis.segments'), (load_leaderboard, 'analysis.leaderboard')]

