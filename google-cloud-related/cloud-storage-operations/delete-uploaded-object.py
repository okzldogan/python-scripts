#!/usr/bin/env python

import os
from google.cloud import storage


# Set the bucket name, source file, and destination folder and blob name

bucket_name = "my-bucket"
destination_folder = "my-folder/"
object_name = "my-file.txt"
destination_blob_name = destination_folder + object_name



def deleted_object_in_bucket(bucket_name, destination_blob_name):
    """
    Authenticates to google cloud storage and deletes an object in the bucket.
    """

    storage_client = storage.Client()


    # Upload the file to the bucket

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    # Delete the uploaded file from the bucket

    print(f"Deleting file {destination_blob_name} from bucket {bucket_name}...")

    request = blob.delete()

    # If deletion fails, exit the script

    if request == 0:
        print(f"Deleting file {destination_blob_name} from bucket {bucket_name} failed. Exiting script...")
        exit()
    # If deletion succeeds, continue with the script
    else:
        print(f"Deleting file {destination_blob_name} from bucket {bucket_name} succeeded.")
        pass



deleted_object_in_bucket(bucket_name, destination_blob_name)    

