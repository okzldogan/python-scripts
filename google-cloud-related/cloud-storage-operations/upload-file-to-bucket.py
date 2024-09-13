#!/usr/bin/env python

import os
from google.cloud import storage


# Set the bucket name, source file, and destination folder and blob name

bucket_name = "my-bucket"
source_file = "/usr/app/my-source-file.txt"
destination_folder = "my-folder/"

object_name = "my-file.txt"
destination_blob_name = destination_folder + object_name


def upload_file_to_bucket(bucket_name, source_file, destination_blob_name):
    """
    Authenticates to google cloud storage and uploads a file to the bucket.
    """

    storage_client = storage.Client()


    # Upload the file to the bucket

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    print(f"Uploading file {source_file} to {bucket_name}...")

    response = blob.upload_from_filename(source_file)


    # If upload fails, exit the script

    if response == 0:
        print(f"Uploading to {bucket_name} failed. Exiting script...")
        exit()

    # If upload succeeds, continue with the script

    else:
        print(f"Uploading file {destination_blob_name} succeeded.")
        pass


# Call the function

upload_file_to_bucket(bucket_name, source_file, destination_blob_name)