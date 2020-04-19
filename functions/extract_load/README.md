### Strava Extract Load Function

This function is the extract and load to staging parts of the pipeline.

1. Get a message from the pub/sub queue containing a set of coordinates and an activity
2. Call the Strava segment explorer API
3. Get segement details for the 10 segements returned by (2) 
4. Get leaderboard details for the 10 segments returned by (2)
5. Write (4) and (5) to a GCS bucket
6. Write (4) and (5) to a staging table in BigQuery 