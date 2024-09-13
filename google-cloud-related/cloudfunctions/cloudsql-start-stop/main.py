import base64
import json
from googleapiclient.discovery import build

def process_pubsub(event, context):
    """
    Starts and stops a cloudsql instance based on the received pubsub message in JSON format
    """
    # Decode the pubsub message
    message = base64.b64decode(event['data']).decode('utf-8')

    # Print the message

    print(f"Received pubsub message: {message}")

    # Extract the instance name using json.loads
    instance = json.loads(message)['Instance']
    # Extract the project name
    project = json.loads(message)['Project']
    # Extract the action
    action = json.loads(message)['Action']

    print(f"Instance: {instance}")

    # Create the cloudsql API client with the provided credentials

    service = build('sqladmin', 'v1beta4')

    print("Authenticated to SQL Admin API")

    if action == "start":
        action = "ALWAYS"
    elif action == "stop":
        action = "NEVER"
    else:
        print("Invalid action. Must be START or STOP")
        return

    print(f"Action: {action}")

    # # Set the request body for the cloudsql API client

    request_body = {
        'settings': {
            'activationPolicy': f"{action}"
        }
    }

    print(f"printing request body {request_body}")

    # Execute the request

    print(f"Setting activation policy of instance {instance} to {action}...")

    request = service.instances().patch(project=project, instance=instance, body=request_body)

    # Print the response

    response = request.execute()

    # Check the response

    print(response)


