import googleapiclient.discovery
import base64
from json import loads
from datetime import datetime

def create_disk_snapshot(event, context):
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

    # Set the disk info from the pubsub message
    disk_info = loads(message)['Disks']


    # Create the Compute Engine API client with the provided credentials
    compute = googleapiclient.discovery.build('compute', 'v1')

    print("Compute Engine API client created.")


    # Get the date with time
    date = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

    for disk_name, disk in disk_info.items():

        print(f"Snapshotting disk {disk_name}...")
        print(f"Disk type: {disk['type']}")


        if disk['type'] == "regional":

            request_body = {
                'name': f"{disk_name}-snapshot-regional-disk--{date}",
                'description': f"Snapshot of regional disk {disk_name} on {date} with Cloud Function",
                'storageLocations': f"{disk['storage_location']}",
                'labels': {
                    'created-by': 'cloud-function',
                    'type': f"{disk['mounted_vm']}"
                }
            }

            operation = compute.regionDisks().createSnapshot(project=project_id, region=disk["region"], disk=disk_name, body=request_body).execute()

        elif disk['type'] == "zonal":

            request_body = {
                'name': f"{disk_name}-snapshot-zonal-disk--{date}",
                'description': f"Snapshot of regional disk {disk_name} on {date} with Cloud Function",
                'storageLocations': f"{disk['storage_location']}",
                'labels': {
                    'created-by': 'cloud-function',
                    'type': f"{disk['mounted_vm']}"
                }
            }

            operation = compute.disks().createSnapshot(project=project_id, zone=disk["zone"], disk=disk_name, body=request_body).execute()

        print(f"Snapshotting disk {disk_name} with {disk['type']} disk type ...done.")

