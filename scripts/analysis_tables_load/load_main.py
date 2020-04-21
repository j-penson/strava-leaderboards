"""Create analytics tables in BigQuery.

:authors
    JP at 19/04/20
"""

from google.cloud import bigquery
from scripts.analysis_tables_load.src.load_queries import load_queries
from scripts.analysis_tables_load.src.check_queries import check_queries

client = bigquery.Client()


def execute_load_query(sql_query):
    """Execute a Bigquery load statement."""
    print(f'Executing load to {sql_query[1]}')
    query_job = client.query(sql_query[0])
    # Wait for execution
    _ = query_job.result()
    return query_job.done()


def get_count(table):
    """Get a row count for the table"""
    count_job = client.query(f'SELECT COUNT(*) row_count FROM {table}')
    result = count_job.result()
    for row in result:
        print(f'{row.row_count} in {table}')


def execute_check_query(sql_query):
    """Execute a Bigquery check statement."""
    print(f'Executing check {sql_query}')
    query_job = client.query(sql_query)
    # Wait for execution
    result = query_job.result()

    if result.total_rows == 0:
        print('check successful')
    else:
        for row in result:
            print(row)
    return query_job.done()


print('counts before')
counts = [get_count(table[1]) for table in load_queries]

print('Executing load queries')
results = [execute_load_query(query) for query in load_queries]

print('counts after')
counts = [get_count(table[1]) for table in load_queries]

print('starting checks')
checks = [execute_check_query(query) for query in check_queries]

