import json
from stravalib.client import Client


client = Client(access_token='6ed5c16298f6bf6b9573a4af83e7dc12903bf507')

# curr_athlete = client.get_athlete()

activity_type = 'riding'

NE = 51.69844, 0.18907  # Toot Hill in Essex
SW = 51.53760, -0.11009  # Islington




bounds = SW + NE

segments = client.explore_segments(bounds=bounds, activity_type=activity_type)

# with open('./sample_data/segment.json', 'w') as f:
#     json.dump(segments[0].segment.to_dict(), f)
#
# with open('./sample_data/segment_result.json', 'w') as f:
#     json.dump(segments[0].to_dict(), f)

