# Declare variables
organization, github_token, headers = "", "", {}


from requests import get
from json import loads
from datetime import datetime, timedelta


def get_all_repos(github_token, organization, headers):

    repo_names = []
    url = f"https://api.github.com/orgs/{organization}/repos"

    per_page = 100
    
    
    for page in range(1, 4):

        response = get(url, headers=headers, params={"per_page": per_page, "page": page})

        if response.status_code==200:
            for repo in response.json():
                # Add all repos to a list
                repo_names.append(repo["name"])
        else:
            print("Something went wrong")
            print(response.content.decode('utf-8'))
            break
    
    return repo_names

# Refactor get_all_repos function to yield repo names insteand of returning a list call the function repo_yielder

def repo_yielder(github_token, organization, headers):
    
        url = f"https://api.github.com/orgs/{organization}/repos"
    
        per_page = 100
        
        for page in range(1, 4):
    
            response = get(url, headers=headers, params={"per_page": per_page, "page": page})
    
            if response.status_code==200:
                for repo in response.json():
                    yield repo["name"]
            else:
                print("Repo names could not be retrieved")
                print(response.content.decode('utf-8'))
                break


def is_repo_archived(github_token, repo_name, organization, headers):

    archival_status = {
        True: "Repo archived",
        False: "Repo not archived"
    }

    url = f"https://api.github.com/repos/{organization}/{repo_name}"
    
    response = get(url, headers=headers)
    
    if response.status_code==200:
        json_response = loads(response.content.decode('utf-8'))
        repo_archive_info = json_response["archived"]

        return archival_status[json_response["archived"]]
            
    else:
        print("Something went wrong")
        print(response.content.decode('utf-8'))
                

def get_workflow_names(github_token, repo_name, organization, headers):

    workflow_names_and_ids = {}
    url = f"https://api.github.com/repos/{organization}/{repo_name}/actions/workflows"
        
    response = get(url, headers=headers)
    
    if response.status_code==200:
        json_response = loads(response.content.decode('utf-8'))
        get_workflows = json_response["workflows"]
        for workflow in get_workflows:
            if None == workflow["name"]:
                workflow_names_and_ids["No workflows"] = "No workflows"
            else:
                workflow_names_and_ids[workflow["name"]] = workflow["id"]

    else:
        print("Something went wrong")
        print(response.content.decode('utf-8'))

    if not workflow_names_and_ids:
        return {"No workflows": "No workflows"}
    else:
        return workflow_names_and_ids

def has_workflow_ever_run(github_token, repo_name, workflow_id, organization, headers):

    if workflow_id == "No workflows":
        return "No workflows in this repo"
    else:

        url = f"https://api.github.com/repos/{organization}/{repo_name}/actions/workflows/{workflow_id}/runs"
            
        response = get(url, headers=headers)
        
        if response.status_code==200:
            json_response = loads(response.content.decode('utf-8'))
            if json_response["total_count"] == 0:
                return False
            else:
                return True

        else:
            print("Something went wrong")
            print(response.content.decode('utf-8'))

def get_workflow_last_run_date(github_token, repo_name, workflow_id, organization, headers):

    check_workflow_run_status = has_workflow_ever_run(github_token, repo_name, workflow_id, organization, headers)

    if check_workflow_run_status == "No workflows in this repo":
        return "Not applicable"

    
    elif check_workflow_run_status == False:
        return "Workflow has never run"

    else:

        url = f"https://api.github.com/repos/{organization}/{repo_name}/actions/workflows/{workflow_id}/runs"
            
        response = get(url, headers=headers)
        
        if response.status_code==200:
            json_response = loads(response.content.decode('utf-8'))
            last_run_date = json_response["workflow_runs"][0]["created_at"]
            # Convert last run date to a datetime object
            last_run_as_date_object = datetime.strptime(last_run_date, "%Y-%m-%dT%H:%M:%SZ")
            # Convert last_run_as_date_object to string
            last_run_as_string = last_run_as_date_object.strftime("%d-%m-%Y")
            return last_run_as_string

        else:
            print("Something went wrong")
            print(response.content.decode('utf-8'))

def get_latest_pull_request(github_token, repo_name, organization, headers):

    pull_request_info = {}

    state       = "all"
    direction   = "desc"

    url = f"https://api.github.com/repos/{organization}/{repo_name}/pulls"

    response = get(url, headers=headers, params={"state": state, "direction": direction})

    if response.status_code==200:
        json_response = loads(response.content.decode('utf-8'))

        if json_response == []:

            pull_request_info["No PR ID Found"] = {
                "title": "No PR title found",
                "created_at": "Not applicable"
            }

            return pull_request_info["No PR ID Found"]
        
        else:

            # Get the latest PR
            get_the_latest_pr = json_response[0]

            pull_request_info[get_the_latest_pr["id"]] = {
                "title": get_the_latest_pr["title"],
                "created_at": get_the_latest_pr["created_at"]
            }



            return pull_request_info[get_the_latest_pr["id"]]


    else:
        print("Something went wrong")
        print(response.content.decode('utf-8'))