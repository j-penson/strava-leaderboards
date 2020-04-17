"""Functions to write to local and Google Cloud Storage.

:authors
    JP at 17/04/20
"""
from google.cloud import storage
import json
import os

storage_client = storage.Client()
bucket = storage_client.bucket(os.environ['STRAVA_BUCKET_NAME'])


def upload_blob_from_file(filepath: str, filename: str, file_type: str):
    """Upload a file to GCS."""
    blob = bucket.blob(os.path.join(file_type, filename))
    blob.upload_from_filename(os.path.join(filepath, filename))
    print(f'file {filename} uploaded file_name')


def upload_blob_from_string(data, filename: str, file_type: str):
    """Upload to GCS from a string."""
    blob = bucket.blob(os.path.join(file_type, filename))
    blob.upload_from_string(json.dumps(data), content_type='application/json')
    print(f'file {filename} uploaded file_name')


def write_to_local(local_dir: str, file_type: str, filename: str, data):
    """Write a dict to a local directory."""
    with open(os.path.join(local_dir, file_type, filename), 'w') as f:
        json.dump(data, f)
