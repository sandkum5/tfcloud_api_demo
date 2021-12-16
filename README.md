# tfcloud_api_demo
Repo to test Terraform Cloud API calls

main.py file will create/list below objects in Terraform Cloud using Terraform Cloud API 
    1. Create Workspaces
    2. List Workspace Names and ID's
    3. Create Workspace Variables
    4. List Workspace Variables
    
Define org info, workspace and variables data in api_data.json 

#### Sample Output

```
% python3 main.py 
Creating workspace: tfcloud_api_demo
Workspace Create Status: 201
Creating WorkSpace Var: Name
Workspace Variable Create Status: 201
Creating WorkSpace Var: Enabled
Workspace Variable Create Status: 201
Creating WorkSpace Var: NtpServers
Workspace Variable Create Status: 201
Creating WorkSpace Var: TimeZone
Workspace Variable Create Status: 201
Creating WorkSpace Var: org_name
Workspace Variable Create Status: 201
Creating WorkSpace Var: Description
Workspace Variable Create Status: 201
```
