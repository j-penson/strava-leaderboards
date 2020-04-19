"""Functions call the Stava API using the client.

:authors
    JP at 17/04/20
"""
import logging
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
    logging.info(f'filename is {filename}')
    return filename


def get_leaderboard_data(segments):
    """Get and expand leaderboard data."""
    leaderboard_list = []

    for segment_item in segments:

        segemnt_dict = segment_item.segment.to_dict()
        leaderboard_dict = segment_item.segment.leaderboard.to_dict()

        # For each entry get the segment information (name, type, distance, coords) and the leaderboard details
        for leader_entry in leaderboard_dict['entries']:
            leader_entry['segment_name'] = segemnt_dict['name']
            leader_entry['segment_activity_type'] = segemnt_dict['activity_type']
            leader_entry['segment_distance'] = segemnt_dict['distance']
            leader_entry['segment_start_latlng'] = segemnt_dict['start_latlng']
            leader_entry['segment_end_latlng'] = segemnt_dict['end_latlng']
            leader_entry['entry_count'] = leaderboard_dict['entry_count']
            leader_entry['effort_count'] = leaderboard_dict['effort_count']
            leader_entry['kom_type'] = leaderboard_dict['kom_type']

            leaderboard_list.append(leader_entry)

    return leaderboard_list


def get_strava_data(sw_lat, sw_lon, ne_lat, ne_lon, activity, api_key):
    """Get segment and leaderboard data for a set of coordinates."""
    coordinates = [sw_lat, sw_lon, ne_lat, ne_lon]

    if sw_lat > ne_lat or sw_lon > ne_lon:
        raise DodgyCoordinates

    logging.info(f'getting data for {coordinates}')

    client = Client(access_token=api_key)

    # TODO refactor this it shouldn't live here
    filename = get_filename(activity, coordinates, grid=False)

    segments = client.explore_segments(bounds=coordinates, activity_type=activity)
    logging.info(f'got {len(segments)} segments')

    if len(segments) == 0:
        logging.info("no segments found")
        raise NoSegmentsFound

    segments_list = [segment_item.segment.to_dict() for segment_item in segments]
    logging.info(f'segments are {segments_list}')

    leaderboard_list = get_leaderboard_data(segments)
    logging.info(f'leaderboard for segments are {leaderboard_list}')

    return segments_list, leaderboard_list, filename
