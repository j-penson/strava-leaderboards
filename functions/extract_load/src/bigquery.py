"""Write to Google BigQuery.

:authors
    JP at 17/04/20
"""
import datetime
import logging
import pandas as pd
import os

SEGMENT_DTYPES = {'name': 'str', 'activity_type': 'str', 'distance': 'float64',
                  'average_grade': 'float64', 'maximum_grade': 'float64',
                  'elevation_high': 'float64', 'elevation_low': 'float64', 'start_latlng': 'str',
                  'end_latlng': 'str', 'start_latitude': 'float64', 'end_latitude': 'float64',
                  'start_longitude': 'float64', 'end_longitude': 'float64',
                  'climb_category': 'int64', 'city': 'str', 'state': 'str', 'country': 'str',
                  'private': 'bool', 'starred': 'bool', 'athlete_segment_stats': 'str',
                  'created_at': 'str', 'updated_at': 'str', 'total_elevation_gain': 'float64',
                  'map': 'str', 'effort_count': 'int64', 'athlete_count': 'int64',
                  'hazardous': 'bool', 'star_count': 'int64', 'pr_time': 'str',
                  'starred_date': 'float64', 'athlete_pr_effort': 'float64'}

LEADERBOARD_DTYPES = {'athlete_name': 'str', 'elapsed_time': 'str', 'moving_time': 'str',
                      'start_date': 'str', 'start_date_local': 'str', 'rank': 'int64',
                      'segment_name': 'str', 'segment_activity_type': 'str', 'segment_distance': 'float64',
                      'segment_start_latlng': 'str', 'segment_end_latlng': 'str', 'entry_count': 'int64',
                      'effort_count': 'int64', 'kom_type': 'str'}


def write_df(df, table):
    """Write a dataframe to a table in append mode."""
    df['insert_date'] = str(datetime.datetime.now())
    df.to_gbq(table,
              project_id=os.environ['GCP_PROJECT'],
              if_exists='append')
    logging.info(f'written {len(df)} rows to {table}')


def write_to_bq(segments_list, leaderboard_list):
    """Write segments and the leaderboard to BigQuery."""
    df_segment = pd.DataFrame(segments_list)
    df_segment = df_segment.astype(SEGMENT_DTYPES)
    write_df(df=df_segment, table='staging.segments')

    df_leaderboard = pd.DataFrame(leaderboard_list)
    df_leaderboard = df_leaderboard.astype(LEADERBOARD_DTYPES)
    write_df(df=df_leaderboard, table='staging.leaderboard')
