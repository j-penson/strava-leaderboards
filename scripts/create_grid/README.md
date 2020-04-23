# Create grid

The create grid sripts takes a set of coordinated (SW lat, long and NE lat, long) and divided into a grid of equally sized sub-grids.

The coordinates for each sub-grid are pushed to a GCP pubsub queue, in order for the extract_load function to call the Strava API.