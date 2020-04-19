# Strava Leaderboards

A project for the Udacity Data Engineering Nanodegree.

As keen cyclist/runner and Strava user, I'm looking to find interesting segments in my local area (NE London) - popular segments, or those with an achievable KOM/CR. A segment is part of a road or path used by Strava users to compare cycling/running times. The leader of a particular segment is known at the KOM/QOM for cycling and the Course Record holder for running.

Strava has a great API that allows users to search for segments in a particular area based on certain criteria. This project will call the API for my area, store the data in a database

## Data Model

The core of the data model I'm looking to create is as follows:

- Segment times (leaderboards)
- Segment information 
- Locations - coordinates

This can then be joined to other information, such as weather data for analysis.

## Strava API

I'm going to use the API segment explorer to get a list of segments in the area: http://developers.strava.com/docs/reference/#api-Segments-exploreSegments

Then the leaderboard for that segment: http://developers.strava.com/docs/reference/#api-Segments-getLeaderboardBySegmentId

Strava limit API requests 100 requests every minute, 1000 daily, which means I should be able to collect a nice amount of data to analyse.

There's a handy Python client for the Strava API: https://github.com/hozn/stravalib

## Data Pipeline

1. `scripts/create_grid`: split a set of coordinates into a grid of (e.g. 100 lateral points by 50 longintudinal points). Push the coorindates to pub/sub.
2. `functions/extract_load`: a Google Cloud Function to get the data from strava
    - Get a message from the pub/sub topic with a set of coordinates to search
    - Call the [segment explorer](https://developers.strava.com/docs/reference/#api-Segments-exploreSegments) API to get the 10 most popular segments in that area
    - For each segment, get the [segment information](https://developers.strava.com/docs/reference/#api-Segments-getSegmentById)
    - For each segment, get the [leaderboard information](https://developers.strava.com/docs/reference/#api-Segments-getLeaderboardBySegmentId)
    - Write the raw JSON files to Google Cloud Storage
    - Load the data into staging tables in Google BigQuery
3. `functions/strava_key`: a Google Cloud Function to update the Strava access token that expires every 6 hours
4. `scripts/analysis_tables_create`: create the analysis tables in BigQuery
5. `scripts/analysis_tables_load`: load from the staging tables to the analysis tables in BigQuery
 

## Infrastructure/Tooling
GCP is decent for data tooling, I'm using it extensively in this project. 

- BigQuery for target storage/analysis
- Cloud Functions for extracting the data
- Cloud Storage to keep copies of the raw segment data
- Pub/sub for a queue of all the points to calculate
- Cloud Scheduler for orchestrating jobs
- Github Actions for CI

If cost was less important, I'd consider using Cloud Composer (managed Airflow) The tooling I've chosen should scale well, but if the volume of data increased by a few orders of magnitude then I'd look to Dataflow (Apache Beam)


## Scenarios for Udacity Project Rubric (TODO)

1. Data increased by 100x

2. Pipelines run on a daily basis

3. Database needs to be accessed by 100+ people