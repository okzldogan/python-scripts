import base64
from json import loads
import requests
from googleapiclient.discovery import build
from google.cloud import secretmanager


branch="my-branch"
org_name="my-github-organization"
repo="my-github-repo"
workflow_name="my-workflow-file-name.yaml"
workflow_options= [
    "my-option-1",
    "my-option-2",
]
project_id="my-gcp-project"


def trigger_github_action(event, context):
    """
    Triggers a github action from a cloud function
    """
    # Decode the pubsub message
    message = base64.b64decode(event['data']).decode('utf-8')

    message_json = loads(message)

    restarted_container = message_json['incident']['resource']['labels']['container_name']
    print(f"Restarted container: {restarted_container}")

    namespace_of_restarted_container = message_json['incident']['resource']['labels']['namespace_name']
    print(f"Restarted container namespace: {namespace_of_restarted_container}")

    # Iniatiate the GCP secret manager client
    secret_manager_client = secretmanager.SecretManagerServiceClient()


    secret_name = f"projects/{project_id}/secrets/workflow-pat"


    # Set the secret name
    latest_secret_version = f"{secret_name}/versions/latest"

    print("Authenticating to Secret Manager...")

    # Get the secret
    secret_response = secret_manager_client.access_secret_version(request={"name": latest_secret_version})

    # Parse the JSON output of secret_response
    access_secret               = loads(secret_response.payload.data.decode("UTF-8"))
    github_token                = access_secret['github_token']

    url = f"https://api.github.com/repos/{org_name}/{repo}/actions/workflows/{workflow_name}/dispatches"
    
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {github_token}",
        "Content-Type": "application/json",
        "X-GitHub-Api-Version": "2022-11-28" 
    }

    if github_token:
        print("Accessed to github token from the Secret Manager")
        for items in workflow_options:
            data = '{"ref":"'+branch+'","inputs":{"workflow_options":"'+items+'"}}'
        
            response = requests.post(url, headers=headers, data=data)
        
            if response.status_code==204:
                print(f"Workflow for {items} Triggered!")
            else:
                print(f"Something went wrong for the {items} workflow.")
                print(response.text)
        
    else:
        print("Failed to get the github token from the Secret Manager")


