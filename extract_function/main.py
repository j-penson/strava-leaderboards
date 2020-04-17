"""Strava API collector function.

:authors
    JP/MD at 02/01/20
"""
import base64
import os

from src import pubsub_messages
from src import strava_api
from src import write_to_storage
from src import bigquery


def get_strava_data(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic."""
    pubsub_message = base64.b64decode(event['data']).decode('utf-8')
    print(pubsub_message)
    print(os.environ['GCP_PROJECT'])
    print(os.environ['STRAVA_BUCKET_NAME'])
    print(os.environ['STRAVA_API_KEY'])
    print(os.environ['SUB_ID'])
    for _ in range(9):
        ack_id, message_data = pubsub_messages.get_message()

        segments_list, leaderboard_list, filename = strava_api.get_strava_data(**message_data)

        write_to_storage.upload_blob_from_string(data=segments_list, filename=filename, file_type='segments')
        write_to_storage.upload_blob_from_string(data=leaderboard_list, filename=filename, file_type='leaderboard')

        bigquery.write_to_bq(segments_list, leaderboard_list)

        pubsub_messages.ack_message(ack_id)
