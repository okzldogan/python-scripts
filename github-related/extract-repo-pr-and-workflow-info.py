organization = "my-github-org"

github_token = "my-github-token"

headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {github_token}",
    "X-GitHub-Api-Version": "2022-11-28"
}

from datetime import datetime, timedelta
from functions import get_all_repos, is_repo_archived, get_workflow_names
from functions import has_workflow_ever_run, get_workflow_last_run_date
from functions import get_latest_pull_request
import csv

all_repo_names  = get_all_repos(github_token, organization, headers)
add_new_line = "\n"

print(f"Number of repos: {len(all_repo_names)}")


for repo_name in all_repo_names:


    repo_archival_status = is_repo_archived(github_token, repo_name, organization, headers)
    get_last_pr = get_latest_pull_request(github_token, repo_name, organization, headers)
    workflows_in_a_repo = get_workflow_names(github_token, repo_name, organization, headers)

    if get_last_pr["created_at"] == "Not applicable":
        last_pr_as_string = "Not applicable"
    else:
        # Convert get_last_pr["created_at"] to a datetime object
        last_pr_as_date_object = datetime.strptime(get_last_pr["created_at"], "%Y-%m-%dT%H:%M:%SZ")
        # Convert last_pr_as_date_object to string
        last_pr_as_string = last_pr_as_date_object.strftime("%d-%m-%Y")

    if "," in get_last_pr["title"]:
        get_last_pr["title"] = get_last_pr["title"].replace(",", "")

    # Store all the information in a dictionary
    repo_last_pr_info = {
        "repo_name": repo_name,
        "repo_archival_status": repo_archival_status,
        "last_pr_title": get_last_pr["title"],
        "last_pr_date": last_pr_as_string,
    }

    with open("repo-last-pr.csv", "a") as csv_file:
        
        writer = csv.writer(csv_file)
        writer.writerow(repo_last_pr_info.values())


    for workflow_name, workflow_id in workflows_in_a_repo.items():
        
        workflow_last_run_date = get_workflow_last_run_date(github_token, repo_name, workflow_id, organization, headers)

        # If workflow_name contains "," remove it
        if "," in workflow_name:
            workflow_name = workflow_name.replace(",", "")

        with open("info-on-github-repos.csv", "a") as file:
            file.write(",".join([repo_name, repo_archival_status, workflow_name, workflow_last_run_date]) + add_new_line)

