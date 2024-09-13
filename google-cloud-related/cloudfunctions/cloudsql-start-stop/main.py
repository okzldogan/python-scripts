import base64
from json import loads
from googleapiclient.discovery import build

def process_pubsub(event, context):
    """
    Starts and stops a cloudsql instance based on the received pubsub message in JSON format
    """
    # Decode the pubsub message
    message = base64.b64decode(event['data']).decode('utf-8')

    # Print the received message

    print(f"Received pubsub message: {message}")

    # Extract parameters from the message
    instance = loads(message)['Instance']
    project = loads(message)['Project']
    action = loads(message)['Action']

    print(f"Instance: {instance}")


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


