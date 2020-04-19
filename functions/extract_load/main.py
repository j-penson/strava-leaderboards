"""Strava API collector function.

:authors
    JP at 17/04/20
"""
from google.cloud import firestore
import logging
from src import pubsub_messages
from src import strava_api
from src import write_to_storage
from src import bigquery

db = firestore.Client()
collection = db.collection('strava')


def get_strava_data(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic."""
    # For each API key in the database
    for doc in collection.stream():
        data = doc.to_dict()
        api_key = data['access_token']

        logging.info(f'starting get_strava_data for {doc.id}')

        ack_id, message_data = pubsub_messages.get_message()

        api_call_count = 0

        # Get segments until 40 API calls have been made
        while api_call_count < 40:

            try:
                # Get Strava data for the coordinates using the client
                segments_list, leaderboard_list, filename = strava_api.get_strava_data(**message_data, api_key=api_key)

                api_call_count += (1 + len(segments_list) + len(leaderboard_list))
                logging.info(f'api call count for {doc.id} is {api_call_count}')

                # Write the JSON data to GCS
                write_to_storage.upload_blob_from_string(data=segments_list, filename=filename, file_type='segments')
                write_to_storage.upload_blob_from_string(data=leaderboard_list, filename=filename, file_type='leaderboard')

                # Write the BigQuery staging tables
                bigquery.write_to_bq(segments_list, leaderboard_list)

                # Finally acknowledge the message
                pubsub_messages.ack_message(ack_id)

            # If no segments have been found for those coordinates, still acknowledge the message
            except strava_api.NoSegmentsFound:
                api_call_count += 1
                logging.warning(f'no segments found for {data} call count {api_call_count}')
                pubsub_messages.ack_message(ack_id)

            except Exception as e:
                logging.error(f'error with {doc.id}: {data} {e}')
                logging.error(f'error with {doc.id}: {e}')
