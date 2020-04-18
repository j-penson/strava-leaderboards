"""Write to Google BigQuery.

:authors
    JP at 17/04/20
"""
import pandas as pd
import os


def write_df(df, table):
    """Write a dataframe to a table in append mode."""
    df.to_gbq(table,
              project_id=os.environ['GCP_PROJECT'],
              if_exists='append')
    print(f'written {len(df)} rows to {table}')


def write_to_bq(segments_list, leaderboard_list):
    """Write segments and the leaderboard to BigQuery."""
    df_segment = pd.DataFrame(segments_list)
    df_leaderboard = pd.DataFrame(leaderboard_list)

    write_df(df=df_segment, table='staging.segments')
    write_df(df=df_leaderboard, table='staging.leaderboard')
