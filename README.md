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

1. Take a grid of coordinates, and split it into smaller parts (e.g. 100 by 50). Push the coorindates to pub/sub.
2. Deploy a Google Cloud function to pull messages from the queue, call the API
3. Write to json files in Google Cloud Storage, and a staging 


## Infrastructure/Tooling
As I mainly use GCP at work, so I'll use it for this project. To keep costs down I'm planning on using serverless tools where possible.

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