"""Functions call the Stava API using the client.

:authors
    JP at 17/04/20
"""

from stravalib.client import Client


class DodgyCoordinates(Exception):
    """Exception to fail coordinate checks."""

    pass


class NoSegmentsFound(Exception):
    """Exception when Strava doesn't find anything."""

    pass


def get_filename(activity_type: str, coordinates: list, grid: bool, lat_steps=None, lon_steps=None):
    """Build the filename to be written to storage."""
    filename = f'{activity_type}'

    for coord in coordinates:
        filename = filename + f'_{coord:.6f}'

    if grid:
        filename += f'_{lat_steps}_{lon_steps}'

    filename += '.json'
    print(f'filename is {filename}')
    return filename


def get_strava_data(sw_lat, sw_lon, ne_lat, ne_lon, activity, api_key):
    """Get segment and leaderboard data for a set of coordinates."""
    coordinates = [sw_lat, sw_lon, ne_lat, ne_lon]

    if sw_lat > ne_lat or sw_lon > ne_lon:
        raise DodgyCoordinates

    print(f'getting data for {coordinates}')

    client = Client(access_token=api_key)

    # TODO refactor this it shouldn't live here
    filename = get_filename(activity, coordinates, grid=False)

    segments = client.explore_segments(bounds=coordinates, activity_type=activity)
    print(f'got {len(segments)} segments')

    if len(segments) == 0:
        print("no segments found")
        raise NoSegmentsFound

    segments_list = [segment_item.segment.to_dict() for segment_item in segments]
    print(f'segments are {segments_list}')

    leaderboard_list = [segment_item.segment.leaderboard.to_dict() for segment_item in segments]
    print(f'leaderboard for segments are {leaderboard_list}')

    return segments_list, leaderboard_list, filename
