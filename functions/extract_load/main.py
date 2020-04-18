"""Strava API collector function.

:authors
    JP at 17/04/20
"""
from src import pubsub_messages
from src import strava_api
from src import write_to_storage
from src import bigquery


def get_strava_data(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic."""
    # Attempt to get 4 segments and the corresponding leaderboard (100 requests per 15 mins, 21 calls per request)
    for _ in range(4):
        ack_id, message_data = pubsub_messages.get_message()

        segments_list, leaderboard_list, filename = strava_api.get_strava_data(**message_data)

        write_to_storage.upload_blob_from_string(data=segments_list, filename=filename, file_type='segments')
        write_to_storage.upload_blob_from_string(data=leaderboard_list, filename=filename, file_type='leaderboard')

        bigquery.write_to_bq(segments_list, leaderboard_list)

        pubsub_messages.ack_message(ack_id)
