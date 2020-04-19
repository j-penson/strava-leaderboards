"""Create analytics tables in BigQuery

:authors
    JP at 19/04/20
"""

from google.cloud import bigquery
from scripts.analysis_tables_load.src.sql_queries import load_queries, load_segments

client = bigquery.Client()


def execute_query(sql_query):
    """Execute a Bigquery load statement"""
    print(f'Executing {sql_query}')
    query_job = client.query(sql_query)
    # Wait for execution
    _ = query_job.result()
    return query_job.done()


print('Executing load queries')
results = [execute_query(query) for query in load_queries]
