"""Push coordinates to pubsub.

:authors
    JP at 15/04/20
"""
from google.cloud import pubsub_v1
import json
import os

from create_grid import create_coordinates
from extract_function.src.write_to_storage import upload_blob_from_string

project_id = os.environ['GCP_PROJECT']

# Create a pub/sub publisher to push messages to
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, 'dev')

activity = 'riding'

NE = 51.704121, 0.245740  # Chipping Ongar
SW = 51.534969, -0.103750  # Islington

gen_grid = create_coordinates.GenerateGrid(NE, SW, activity)

lat_steps = 6
lon_steps = 5
grid = gen_grid.generate_grid(lat_steps, lon_steps)

# Write the file to GCS as a backup
grid_filename = f'grid_{activity}_{lat_steps}_{lon_steps}_{SW[0]}_{SW[1]}_{NE[0]}_{NE[1]}.json'

grid_json = json.dumps(grid)

with open(os.path.join('../data/grids/', 'grid_riding_21_11_51.534969_-0.10375_51.704121_0.24574.json'), 'w') as f:
    json.dump(grid, f)

upload_blob_from_string(grid_json, grid_filename, 'grids')

for grid_item in grid:
    data = json.dumps(grid_item).encode('utf-8')
    future = publisher.publish(topic_path, data=data)
    print(future.result())
