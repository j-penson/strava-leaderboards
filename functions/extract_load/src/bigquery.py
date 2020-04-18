"""Write to Google BigQuery.

:authors
    JP at 17/04/20
"""
import pandas as pd
import os

SEGMENT_DTYPES = {'name': 'string', 'activity_type': 'string', 'distance': 'float64',
                  'average_grade': 'float64', 'maximum_grade': 'float64',
                  'elevation_high': 'float64', 'elevation_low': 'float64', 'start_latlng': 'string',
                  'end_latlng': 'string', 'start_latitude': 'float64', 'end_latitude': 'float64',
                  'start_longitude': 'float64', 'end_longitude': 'float64',
                  'climb_category': 'int64', 'city': 'string', 'state': 'string', 'country': 'string',
                  'private': 'bool', 'starred': 'bool', 'athlete_segment_stats': 'string',
                  'created_at': 'string', 'updated_at': 'string', 'total_elevation_gain': 'float64',
                  'map': 'string', 'effort_count': 'int64', 'athlete_count': 'int64',
                  'hazardous': 'bool', 'star_count': 'int64', 'pr_time': 'string',
                  'starred_date': 'float64', 'athlete_pr_effort': 'float64'}

LEADERBOARD_DTYPES = {'athlete_name': 'string', 'elapsed_time': 'string', 'moving_time': 'string',
                      'start_date': 'string', 'start_date_local': 'string', 'rank': 'int64',
                      'segment_name': 'string', 'segment_activity_type': 'string', 'segment_distance': 'float64',
                      'segment_start_latlng': 'string', 'segment_end_latlng': 'string', 'entry_count': 'int64',
                      'effort_count': 'int64', 'kom_type': 'string'}


def write_df(df, table):
    """Write a dataframe to a table in append mode."""
    df.to_gbq(table,
              project_id=os.environ['GCP_PROJECT'],
              if_exists='append')
    print(f'written {len(df)} rows to {table}')


def write_to_bq(segments_list, leaderboard_list):
    """Write segments and the leaderboard to BigQuery."""
    df_segment = pd.DataFrame(segments_list)
    df_segment = df_segment.astype(SEGMENT_DTYPES)

    df_leaderboard = pd.DataFrame(leaderboard_list)
    df_leaderboard = df_leaderboard.astype(LEADERBOARD_DTYPES)

    write_df(df=df_segment, table='staging.segments')
    write_df(df=df_leaderboard, table='staging.leaderboard')
