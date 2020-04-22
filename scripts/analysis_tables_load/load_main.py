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
    query_job = client.query(sql_query)
    # Wait for execution
    _ = query_job.result()
    return query_job.done()


def get_count(table):
    """Get a row count for the table."""
    count_job = client.query(f'SELECT COUNT(*) row_count FROM {table}')
    result = count_job.result()
    for row in result:
        print(f'{row.row_count} in {table}')


def delete_from_table(table):
    """Delete all rows from a table."""
    # Check we're deleting the anlaysis tables and not the staging tables as they'll be time consumng to load
    if 'staging' in table:
        raise ValueError
    delete_job = client.query(f'DELETE FROM {table} WHERE 1=1')
    result = delete_job.result()
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


# For each load query, check row counts, delete rows if specified, load the table then count rows again
for query in load_queries:
    sql_query = query[0]
    table_name = query[1]
    delete_first = query[2]

    if delete_first:
        delete_from_table(table_name)

    print('row count before')
    get_count(table_name)

    print(f'Executing load to {table_name}')
    execute_load_query(sql_query)

    print('row count after')
    get_count(table_name)

print('starting checks')
checks = [execute_check_query(query) for query in check_queries]
