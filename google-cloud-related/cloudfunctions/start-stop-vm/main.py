import googleapiclient.discovery
import base64
from json import loads

def start_stop_vm(event, context):
    """
    Starts & Stops a VM getting the VM name from the pubsub message in JSON format
    """

    # Decode the pubsub message
    message = base64.b64decode(event['data']).decode('utf-8')

    # Print the message
    print(f"Received pubsub message: {message}")

    # Set the project ID from the pubsub message
    project_id = loads(message)['Project']
    # Set the vm name from the pubsub message
    vm_name = loads(message)['VM-Name']
    # Set the vm name from the pubsub message
    vm_zone = loads(message)['VM-Zone']
    # Set the action from the pubsub message
    action = loads(message)['Action']

    print(f"Project ID: {project_id}")

    # Create the Compute Engine API client with the provided credentials
    compute = googleapiclient.discovery.build('compute', 'v1')

    print("Compute Engine API client created.")

    # If action is "stop" then stop the VM

    if action == "stop":    
        request = compute.instances().stop(project=project_id, zone=vm_zone, instance=vm_name)
        response = request.execute()
        print(f"VM {vm_name} is stopped.")

    # If action is "start" then start the VM

    elif action == "start":
        request = compute.instances().start(project=project_id, zone=vm_zone, instance=vm_name)
        response = request.execute()
        print(f"VM {vm_name} is started.")



