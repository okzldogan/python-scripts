import googleapiclient.discovery
import base64
from json import loads
from datetime import datetime, timedelta

def delete_disk_snapshots(event, context):
    """
    Takes a snapshot of a disk based on a pubsub message in JSON format
    """

    # Decode the pubsub message
    message = base64.b64decode(event['data']).decode('utf-8')

    # Print the message
    print(f"Received pubsub message: {message}")

    # Set the project ID from the pubsub message
    project_id = loads(message)['Project']

    print(f"Project ID: {project_id}")

    # Create the Compute Engine API client with the provided credentials
    compute = googleapiclient.discovery.build('compute', 'v1')

    print("Compute Engine API client created.")

    # Get the date
    date = datetime.now().strftime("%Y-%m-%d")

    # Get the time delta for 15 days
    fifteen_days_ago = datetime.now() - timedelta(days=15)

    print(f"Timestamp 15 days ago: {fifteen_days_ago}")

    # Get the snapshots and their timestamps
    disk_snapshots = compute.snapshots().list(project=project_id).execute()

    for disk_snapshot in disk_snapshots['items']:

        # Get the snapshot size
        snapshot_size_in_bytes = int(disk_snapshot['storageBytes'])

        # Convert the snapshot size to GB
        snapshot_size_in_gb = snapshot_size_in_bytes / 1024 / 1024 / 1024

        # Get the date from the timestamp
        snapshot_date = disk_snapshot['creationTimestamp'].split("T")[0]

        # If snapshot date is older than 15 days, delete it
        if datetime.strptime(snapshot_date, "%Y-%m-%d") < fifteen_days_ago:
            print(f"Deleting snapshot {disk_snapshot['name']} with Timestamp: {disk_snapshot['creationTimestamp']} and snapshot size: {snapshot_size_in_gb} GB")
            operation = compute.snapshots().delete(project=project_id, snapshot=disk_snapshot['name']).execute()
            print(f"Snapshot {disk_snapshot['name']} deleted.")