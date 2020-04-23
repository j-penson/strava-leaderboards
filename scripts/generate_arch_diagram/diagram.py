"""Create architecture diagram for data pipeline.

:authors
    JP at 19/04/20
"""
from diagrams import Cluster, Diagram
from diagrams.gcp.analytics import PubSub
from diagrams.gcp.compute import Functions
from diagrams.gcp.storage import GCS
from diagrams.gcp.analytics import BigQuery
from diagrams.gcp.database import Firestore
from diagrams.gcp.devtools import Scheduler

with Diagram("Strava Leaderboard Architecture Diagram ", show=True):
    source = Functions("generate grid")

    with Cluster("Data Pipeline"):
        gird_queue = PubSub("grid queue")

        credential = Firestore("credentials store")

        store = GCS("raw JSON")

        with Cluster("Extract-Load"):
            with Cluster("scheduler"):
                scheduler = Scheduler("scheduler")
                schedule_queue = PubSub("schedule queue")

            extract_load = Functions("worker")

            staging = BigQuery("BigQuery staging dataset")

        with Cluster("Transform"):
            transform = Functions("transform worker")
            analysis = BigQuery("BigQuery analysis dataset")

    scheduler >> schedule_queue >> extract_load
    source >> gird_queue >> extract_load
    credential >> extract_load
    extract_load >> store
    extract_load >> staging >> transform >> analysis
