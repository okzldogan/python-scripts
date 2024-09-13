#!/usr/bin/env python


from google.cloud import storage

# Set the bucket name

bucket_name = "my-bucket"


def list_objects_in_bucket(bucket_name):
    """
    Authenticates to google cloud storage and lists objects in the bucket.
    """

    storage_client = storage.Client()

    # List objects in the bucket

    bucket_objects = storage_client.list_blobs(bucket_name)

    # Return the list of objects in the bucket

    for objects in bucket_objects:
        print(objects.name)

list_objects_in_bucket(bucket_name)