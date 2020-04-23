"""Create a grid of coordinates and push to pub/sub.

:authors
    JP at 15/04/20
"""
from google.cloud import pubsub_v1
import json
import os
import random

from scripts.create_grid.src import create_coordinates
from functions.extract_load.src.write_to_storage import upload_blob_from_string

project_id = os.environ['GCP_PROJECT']
topid_id = os.environ['SUB_ID']

# Create a pub/sub publisher to push messages to
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topid_id)

if __name__ == '__main__':

    activity = 'riding'

    # NE = 51.704121, 0.245740  # Chipping Ongar
    # SW = 51.534969, -0.103750  # Islington

    NE = 51.783457, 0.354545  # Good Easter (Chelmsford)
    SW = 51.386366, -0.329773  # Thames Ditton

    gen_grid = create_coordinates.GenerateGrid(NE, SW, activity)

    lat_steps = 33
    lon_steps = 33
    grid = gen_grid.generate_grid(lat_steps, lon_steps)

    # Shuffle the grid to get an even spread
    random.shuffle(grid)

    # Write the file to GCS as a backup
    grid_filename = f'grid_{activity}_{lat_steps}_{lon_steps}_{SW[0]}_{SW[1]}_{NE[0]}_{NE[1]}.json'

    grid_json = json.dumps(grid)

    upload_blob_from_string(grid_json, grid_filename, 'grids')

    # Publist each grid item to the pubsub queue
    for grid_item in grid:
        data = json.dumps(grid_item).encode('utf-8')
        future = publisher.publish(topic_path, data=data)
        print(future.result())
