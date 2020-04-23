"""SQL statements to create analytics tables.

:authors
    JP at 19/04/20
"""

drop_segments = "DROP TABLE IF EXISTS analysis.dim_segment"
drop_leaderboard = "DROP TABLE IF EXISTS analysis.fact_leaderboard"
drop_start_time = "DROP TABLE IF EXISTS analysis.dim_start_time"

create_segments = """
create table analysis.dim_segment(
    segment_id STRING NOT NULL,
    name STRING NOT NULL,
    activity_type STRING NOT NULL,
    distance FLOAT64 NOT NULL,
    average_grade FLOAT64,
    maximum_grade FLOAT64,
    elevation_high FLOAT64,
    elevation_low FLOAT64,
    start_latlng STRING,
    end_latlng STRING,
    start_latitude FLOAT64,
    end_latitude FLOAT64,
    start_longitude FLOAT64,
    end_longitude FLOAT64,
    climb_category INT64,
    city STRING,
    state STRING,
    country STRING,
    private BOOLEAN,
    starred BOOLEAN,
    created_at STRING,
    updated_at STRING,
    total_elevation_gain FLOAT64,
    map STRING,
    effort_count INT64,
    athlete_count INT64,
    hazardous BOOLEAN,
    star_count INT64,
    pr_time STRING,
    starred_date FLOAT64,
    athlete_pr_effort FLOAT64)
"""

create_leaderboard = """
create table analysis.fact_leaderboard(
    leaderboard_id STRING NOT NULL,
    segment_id STRING NOT NULL,
    elapsed_time TIME,
    elapsed_time_seconds INT64,
    segment_distance_m FLOAT64,
    speed_ms FLOAT64,
    speed_kph FLOAT64,
    start_date TIMESTAMP,
    rank INT64 NOT NULL
);
"""

create_start_time = """
create table analysis.dim_start_time
(
    start_date DATE,
    year INT64,
    month INT64,
    day INT64,
    week_of_year INT64,
    quarter INT64,
    year_month STRING
);
"""

drop_queries = [drop_segments, drop_leaderboard, drop_start_time]
create_queries = [create_segments, create_leaderboard, create_start_time]
