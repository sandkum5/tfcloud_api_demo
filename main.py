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


def create_workspace(org_name, tfcloud_api_token, payload):
    """
    Function to create workspace in tfcloud in the provided organization with Intersight hyperlink
    """
    headers = {
        "Content-Type": "application/vnd.api+json",
        "Authorization": "Bearer " + tfcloud_api_token,
    }
    url = f"https://app.terraform.io/api/v2/organizations/{org_name}/workspaces"
    response = requests.post(
        url,
        headers=headers,
        data=json.dumps(payload),
    )
    # print(response.json())
    print(f"Workspace Create Status: {response.status_code}")


def update_workspace(workspace_id, payload):
    """
    ** Doesn't Work
    Function to create a workspace under the provided organization
    """
    # workspace_name = ""
    # organization_name = ""
    # url = f"https://app.terraform.io/api/v2/organizations/{organization_name}/workspaces/{workspace_name}"
    headers = {
        "Content-Type": "application/vnd.api+json",
        "Authorization": "Bearer O2hKX3r8zakeOQ.atlasv1.QbAlExUIoSAoVMdmmzIxW5Js5LS2LFnQbnG1FydnJgBBWBcNAW5OK81way89ZmSm1xU",
    }
    url = f"https://app.terraform.io/api/v2/workspaces/{workspace_id}"
    response = requests.patch(
        url,
        headers=headers,
        data=json.dumps(payload),
    )
    print(response.json())
    print(f"Workspace Create Status: {response.status_code}")


def get_workspace(tfcloud_api_token, org_name):
    """
    Function to list workspaces under an Organization
    """
    workspace_data = {}
    headers = {
        "Content-Type": "application/vnd.api+json",
        "Authorization": "Bearer " + tfcloud_api_token,
    }
    url = f"https://app.terraform.io/api/v2/organizations/{org_name}/workspaces"
    response = requests.get(
        url,
        headers=headers,
    )
    response_data = response.json()
    for workspace in response_data["data"]:
        workspace_id = workspace["id"]
        workspace_data[workspace_id] = workspace["attributes"]["name"]
    return workspace_data


def create_workspace_var(tfcloud_api_token, workspace_id, payload):
    """
    Function to create variables under workspaces
    """
    headers = {
        "Content-Type": "application/vnd.api+json",
        "Authorization": "Bearer " + tfcloud_api_token,
    }
    url = f"https://app.terraform.io/api/v2/workspaces/{workspace_id}/vars"
    response = requests.post(
        url,
        headers=headers,
        data=json.dumps(payload),
    )
    print(f"Workspace Variable Create Status: {response.status_code}")


def create_workspace_vars(tfcloud_api_token, workspace_id, var_list):
    """
    Function to create multiple variables in a workspace
    """
    for var in var_list:
        payload = {
            "data": {
                "type": "vars",
                "attributes": {
                    "key": var["key"],
                    "value": var["value"],
                    "description": var["description"],
                    "category": var["category"],
                    "hcl": False,
                    "sensitive": False,
                },
            }
        }
        var_name = payload["data"]["attributes"]["key"]
        print(f"Creating WorkSpace Var: {var_name}")
        create_workspace_var(tfcloud_api_token, workspace_id, payload)


def main():
    """
    Main Function to execute the code
    """
    tfcloud_api_token = os.getenv("tfcloud_api_token")

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
    create_workspace(org_name, tfcloud_api_token, workspace_payload)

    # List workspaces
    workspace_data = get_workspace(tfcloud_api_token, org_name)

    # Set workspace ID for which we are creating variables
    for key, value in workspace_data.items():
        if value == workspace_payload["data"]["attributes"]["name"]:
            workspace_id = key

    # Set Variables Payload
    var_list = data["vars"]

    # Create variables defined in tfcloud_vars.json file
    create_workspace_vars(tfcloud_api_token, workspace_id, var_list)


if __name__ == "__main__":
    main()
