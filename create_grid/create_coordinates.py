#!/usr/bin/python
# coding=utf-8
"""Generate coordinate grid.

:authors
    JP at 15/04/20
"""
import numpy as np
import pandas as pd
from typing import Tuple


class GenerateGrid:
    """Generate a grid for an area of coordinates."""

    def __init__(self, ne_coordinates: Tuple[float, float], sw_coordindates: Tuple[float, float], activity: str):
        """Generate a grid for an area with SW and NE corners.

        :param ne_coordinates: lat, long of North East point of grid
        :param sw_coordindates: lat, long of North East point of grid
        """
        print(f'Generating grid from {sw_coordindates} to {ne_coordinates}')
        self.lat_upper = ne_coordinates[0]
        self.lon_upper = ne_coordinates[1]
        self.lat_lower = sw_coordindates[0]
        self.lon_lower = sw_coordindates[1]
        self.activity = activity

    def generate_grid(self, lat_step: int, lon_step: int) -> pd.DataFrame:
        """Generate a grid split by a range of points along the lat and lon.

        :param lat_step: # steps to split latitude
        :param lon_step: # steps to split longitude
        :return: DataFrame of grids of shape (1,lat_step*lon_step)
        """
        print(f'Generating a grid with {(lat_step-1)*(lon_step-1)} points.')

        lat_diff = self.lat_upper - self.lat_lower
        lon_diff = self.lon_upper - self.lon_lower

        lat_range = np.arange(self.lat_lower, self.lat_upper, lat_diff / lat_step)
        lon_range = np.arange(self.lon_lower, self.lon_upper, lon_diff / lon_step)

        grid = []

        # Iterate through the lat and lon ranges. Append to the list the SW coordinate and the NE coordinate.
        for i_lat, lat in enumerate(lat_range):
            # At the highest latitude, the grid is complete
            if i_lat < lat_step - 1:
                for i_lon, lon in enumerate(lon_range):
                    # At the highest longitude, move to the next latitude
                    if i_lon < lon_step - 1:
                        grid.append({'sw_lat': lat,
                                     'sw_lon': lon,
                                     'ne_lat': lat_range[i_lat + 1],
                                     'ne_lon': lon_range[i_lon + 1],
                                     'activity': self.activity})

        print(f'Generated a grid with {len(grid)} points.')

        return grid
