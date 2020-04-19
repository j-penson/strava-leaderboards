"""Create analytics tables in BigQuery

:authors
    JP at 19/04/20
"""

from google.cloud import bigquery
from scripts.analysis_tables_create.src.sql_queries import drop_queries, create_queries

client = bigquery.Client()


def execute_query(sql_query):
    """Execute a Bigquery statement"""
    print(f'Executing {sql_query}')
    query_job = client.query(sql_query)
    # Wait for execution
    _ = query_job.result()
    return query_job.done()


print('Executing drop queries')
results = [execute_query(query) for query in drop_queries]

print('Executing create queries')
results = [execute_query(query) for query in create_queries]
