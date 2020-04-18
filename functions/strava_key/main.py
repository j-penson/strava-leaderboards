"""Strava API key update.

:authors
    JP at 17/04/20
"""
from google.cloud import firestore
import requests
import time

db = firestore.Client()
collection = db.collection('strava')


class RefreshTokenBadRequest(Exception):
    """Expection for an invalid request to Strava to get a new token."""

    pass


def refresh_key(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic. Update Strava keys stored in Firestore."""
    for doc in collection.stream():
        data = doc.to_dict()
        print(f'got key {doc.id}')

        if time.time() < data['expires_at']:
            print(f'expiry time {data["expires_at"]} not greater than current {time.time()}')
            continue
        else:
            print(f'expiry time {data["expires_at"]} greater than current so getting a new access token')

        request_params = {'client_id': data['client_id'],
                          "client_secret": data['client_secret'],
                          "grant_type": "refresh_token",
                          "refresh_token": data['refresh_token']}

        response = requests.post("https://www.strava.com/api/v3/oauth/token", params=request_params)

        print(f'made request to Strava and got response code {response.status_code}')

        if response.status_code != 200:
            raise RefreshTokenBadRequest

        response_dict = response.json()

        update_doc = collection.document(doc.id)

        update_doc.update({'access_token': response_dict['access_token'],
                           'refresh_token': response_dict['refresh_token'],
                           'expires_at': response_dict['expires_at']})

        print(f'updated {doc.id} with new expiry time {response_dict["expires_at"]}')
