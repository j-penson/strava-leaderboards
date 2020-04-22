"""Interaction with pub/sub.

:authors
    JP at 17/04/20
"""
from google.cloud import pubsub_v1
import logging
import json
import os

project_id = os.environ['GCP_PROJECT']
sub_id = os.environ['SUB_ID']

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, sub_id)


class NoMessages(Exception):
    """Custom exception to raise when there aren't any messages to process."""

    pass


def get_message():
    """Get a single message from the PubSub Queue."""
    message_response = subscriber.pull(subscription_path, max_messages=1)
    if len(message_response.received_messages) == 0:
        logging.warning("no messages received")
        raise NoMessages

    received_message = message_response.received_messages[0]
    message_data = json.loads(received_message.message.data)
    logging.info(f'got message {message_data}')
    return received_message.ack_id, message_data


def ack_message(ack_id):
    """Acknowledge a message so it's not redelivered."""
    logging.info(f'acking {subscription_path}, {ack_id}')
    subscriber.acknowledge(subscription=subscription_path, ack_ids=[ack_id])
