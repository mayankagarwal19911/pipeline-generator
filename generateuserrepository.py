import requests
import json

def generateUserRepository(user_request: dict, token: any) -> None:
    response = requests.post(
        "https://api.github.com/user/repos",
        data=json.dumps({"name":user_request["repository_name"]}),
        headers={"Accept":"application/vnd.github+json","Authorization":"Bearer "+token},
    )

    print(response.json())
