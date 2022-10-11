from typing import Dict
import requests
import json

def generateUserRepository(user_request: dict, token: any) -> Dict:
    print("Generating new user repository.")
    try:
        response = requests.post(
        "https://api.github.com/user/repos",
        data=json.dumps({"name":user_request["repository_name"]}),
        headers={"Accept":"application/vnd.github+json","Authorization":"Bearer "+token},
        )
        print(response)
        return response.json()
    except Exception as e:
        print("Failed to clone template to user repository. ", str(e))
