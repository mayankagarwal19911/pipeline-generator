import requests
import json
import sys

def generateUserRepository(user_request: dict, token: any) -> any:
    response = requests.post(
        "https://api.github.com/user/repos",
        data=json.dumps({"name":user_request["repository_name"]}),
        headers={"Accept":"application/vnd.github+json","Authorization":"Bearer "+token},
    )

    return response.json()["git_url"]

if __name__ == '__main__': 
    user_request = sys.argv[1]
    user_token = sys.argv[2]
    json_acceptable_string = user_request.replace("'", "\"")
    user_request = json.loads(json_acceptable_string)

    generateUserRepository(user_request, user_token)
