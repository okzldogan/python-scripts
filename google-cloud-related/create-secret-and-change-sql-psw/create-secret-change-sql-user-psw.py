#!/usr/bin/env python

from os import system
from sys import path
path.append("../random-psw")
from password_generator import generate_password
from google.cloud import secretmanager
from json import dumps



class User:
    all_objects = []

    def __init__(self, project_id, username, host, database):
        self.project_id = project_id
        self.username = username
        self.database = database
        self.host = host
        self.password = generate_password()
        User.all_objects.append(self.username)

    def create_template(self):
        self = {
            "username":f"{self.username}",
            "password":f"{self.password}",
            "host":f"{self.host}",
            "database":f"{self.database}"
        }
        # Convert to JSON
        json_data = dumps(self, indent=4)

        print("JSON Template created...")

        return json_data

    def change_cloudsql_user_password(self):
        """
        Change the password of the user in the cloudsql instance
        """
        cloudsql_instance_id = f"{self.project_id.split('-')[0]}-{self.host.split('.')[0]}-{self.project_id.split('-')[2]}"
        print(f"Changing password for {self.username} user in the {cloudsql_instance_id} at project {self.project_id}")

        change_sql_password_command = f"gcloud sql users set-password {self.username} --instance={cloudsql_instance_id} --password={self.password} --project={self.project_id} --host=%"
        
        run_command = system(change_sql_password_command)

        if run_command == 0:
            print(f"Password changed successfully for {self.username} in the {cloudsql_instance_id} instance!")
        else:
            print(f"Failed to change password for {self.username} in the {cloudsql_instance_id} instance!")


    # Create GCP Secret
    def create_gcp_secret(self):
        """
        Create a secret in Google Cloud Secret Manager
        """
        print(f"Creating secret for {self.username} in the {self.project_id} project...")
        print("Authenticating to Google Cloud Secret Manager...")
        secret_manager_client = secretmanager.SecretManagerServiceClient()
        secret_name = f"cloudsql-{self.username}-db-credentials"


        select_locations = {
            "prod": "europe-west1,europe-north1",
            "staging": "europe-west1",
            "dev": "europe-west1"
        }

        locations = select_locations[self.project_id.split("-")[2]]

        # Iniatite the creation of the secret
        insert_secret = secret_manager_client.create_secret(
            {
                "parent": f"projects/{self.project_id}",
                "secret_id": f"{secret_name}",
                "secret": {
                    "replication": {
                        "user_managed": {
                            "replicas": [
                                {
                                    "location": f"{locations}"
                                }
                            ]
                        }
                    }
                }
            }
        )

        def add_secret_label(self, secret_id=secret_name):
            """
            Add labels to the secret
            """
            
            secret_name = secret_manager_client.secret_path(self.project_id, secret_id)

            print(f"Adding secret labels to {secret_name} secret...")

            labels_to_add = {
                "application": f"{self.project_id.split('-')[1]}",
                "environment": f"{self.project_id.split('-')[2]}",
            }

            labels_request_body = {
                "name": secret_name,
                "labels": labels_to_add
            }

            update_mask = {
                "paths" : ["labels"]
            }

            response = secret_manager_client.update_secret(
                request= {
                    "secret": labels_request_body,
                    "update_mask": update_mask
                }
            )

            if response:
                print(f"Labels added to secret {secret_name} successfully!")
            else:
                print(f"Failed to add labels to secret {secret_name}")

        ###################
        ## Insert secret ##
        ###################

        if insert_secret:
            print(f"Secret {secret_name} created successfully!")
            print("-----------------------------------")

            # Insert secret version

            print(f"Creating secret version for {secret_name}...")
            json_data = self.create_template()

            insert_secret_version = secret_manager_client.add_secret_version(
                {
                    "parent": f"{insert_secret.name}",
                    "payload": {
                        "data": json_data.encode("UTF-8")
                    }
                }
            )

            if insert_secret_version:
                print(f"Secret version created successfully for {secret_name}!")
                print("-----------------------------------")
                add_secret_label(self)

        else:
            print(f"Failed to create secret {secret_name}")

        # Change the password in the cloudsql instance

        self.change_cloudsql_user_password()

# Initiate an object in the User class with the following parameters

my_user = User("my-gcp-project", "my_sql_user", "my-db-instance-name.my-gke-cluster.local" ,"my_db_name").create_gcp_secret()
