#!/usr/bin/env python3

"""
Python program to create/list below objects in Terraform Cloud using Terraform Cloud API 
    1. Create Workspaces
    2. List Workspace Names and ID's
    3. Create Workspace Variables
    4. List Workspace Variables
"""
import os
import json
import requests

from intersight_auth import IntersightAuth
from dotenv import load_dotenv

load_dotenv()


def api_request(PATH, METHOD, PAYLOAD=None):
    """
    Generic Function to make API Calls to Terraform Cloud
    """
    TFCLOUD_API_TOKEN = os.getenv("tfcloud_api_token")
    BASE_URL = "https://app.terraform.io/api/v2/"
    URL = f"{BASE_URL}{PATH}"
    HEADERS = {
        "Content-Type": "application/vnd.api+json",
        "Authorization": "Bearer " + TFCLOUD_API_TOKEN,
    }
    response = requests.request(
        method=METHOD, url=URL, headers=HEADERS, data=json.dumps(PAYLOAD)
    )
    return response


def workspace_create(org_name, payload):
    """
    Function to create workspace in tfcloud in the provided organization with Intersight hyperlink
    """
    path = f"organizations/{org_name}/workspaces"
    response = api_request(PATH=path, METHOD="POST", PAYLOAD=payload)
    print(f"Workspace Create Status: {response.status_code}")


def workspace_get(org_name):
    """
    Function to list workspaces under an Organization
    """
    workspace_data = {}
    path = f"organizations/{org_name}/workspaces"
    response = api_request(PATH=path, METHOD="GET")
    response_data = response.json()
    for workspace in response_data["data"]:
        workspace_id = workspace["id"]
        workspace_data[workspace_id] = workspace["attributes"]["name"]
    return workspace_data


def workspace_variable_create(workspace_id, payload):
    """
    Function to create variables under workspaces
    """
    path = f"workspaces/{workspace_id}/vars"
    response = api_request(PATH=path, METHOD="POST", PAYLOAD=payload)
    print(f"Workspace Variable Create Status: {response.status_code}")


def workspace_variables_create_multi(workspace_id, variable_list):
    """
    Function to create multiple variables in a workspace
    """
    for variable in variable_list:
        payload = {
            "data": {
                "type": "vars",
                "attributes": {
                    "key": variable["key"],
                    "value": variable["value"],
                    "description": variable["description"],
                    "category": variable["category"],
                    "hcl": False,
                    "sensitive": False,
                },
            }
        }
        variable_name = payload["data"]["attributes"]["key"]
        print(f"Creating WorkSpace Var: {variable_name}")
        workspace_variable_create(workspace_id, payload)


def main():
    """
    Main Function to execute the code
    """
    variable_file = "tfcloud_vars.json"
    with open(variable_file, "r") as file:
        data = json.load(file)

    # Set Organization Name
    org_name = data["organization"]

    # Set Workspace Payload
    workspace_payload = data["workspace"]["payload"]

    # Add Intersight Account Moid LINK
    source_url = os.getenv("intersight_account_access_link")
    workspace_payload["data"]["attributes"]["source-url"] = source_url

    # Add VCS Repo OAuth Token ID
    vcs_repo_oauth_token = os.getenv("vcs_repo_oauth_token")
    workspace_payload["data"]["attributes"]["vcs-repo"][
        "oauth-token-id"
    ] = vcs_repo_oauth_token

    # Create Workspace
    workspace_name = workspace_payload["data"]["attributes"]["name"]
    print(f"Creating workspace: {workspace_name}")
    workspace_create(org_name, workspace_payload)

    # List workspaces
    workspace_data = workspace_get(org_name)

    # Set workspace ID for which we are creating variables
    for key, value in workspace_data.items():
        if value == workspace_payload["data"]["attributes"]["name"]:
            workspace_id = key

    # Set Variables Payload
    variable_list = data["vars"]

    # Create variables defined in tfcloud_vars.json file
    workspace_variables_create_multi(workspace_id, variable_list)


if __name__ == "__main__":
    main()
