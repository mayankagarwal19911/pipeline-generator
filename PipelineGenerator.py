import yaml
import json 
import base64
import requests
import sys
from generateuserrepository import generateUserRepository
from cloneapplicationtemplatetouserrepository import cloneApplicationTemplateToUserRepository

in_file = ""
# out_file = "template.yaml" 

def generateWorkflowFromJsonTemplate(json_decoded: dict)-> any:
    print("Generating workflow YAML file from json template.")
    with open(in_file, 'r') as json_in: # , open(out_file, "w") as yaml_out:
        # json_payload = json.load(json_decoded)
        template_yaml = yaml.dump(json_decoded, sort_keys=False)
        base64_encoded_data = base64.b64encode(bytes(template_yaml, "utf-8"))
        base64_str = base64_encoded_data.decode('utf-8')
    
    # with open(out_file, 'w') as filehandle:
    #     filehandle.write(template_yaml)
    return base64_str

def commitWorkFlowFileToUserRepository(user_request: dict, base64_encoded_data: any, gh_token: any):
    print("Committing github actions workflow file to user repository")
    response = requests.put(
        "https://api.github.com/repos/"+user_request["repository_user"]+"/"+user_request["repository_name"]+"/contents/.github/workflows/"+user_request["repository_name"]+"-actions.yaml",
        data=json.dumps({"message":"Template generated by LBG PE Template Generator",
                         "committer":{"name":user_request['repository_user'],
                         "email":user_request['email']},
                         "content":base64_encoded_data,
                         "branch": "master"}),
        headers={"Accept":"application/vnd.github+json","Authorization":"Bearer "+gh_token},
    )
    print(response.json())


def updateTemplateJsonForUserJson(user_request: dict)-> any:
    print("Updating template workflow json based on user request.")
    with open(in_file) as json_file:
        wf_template_json = json.load(json_file)

    wf_template_json['env']['namespace'] = user_request["namespace_name"]
    return wf_template_json



if __name__ == '__main__': 
    user_request = json.loads(sys.argv[1].replace("'", "\""))
    gh_token = sys.argv[2]
    if user_request["app_type"] == 'java':
        in_file = "templates/wf-template-java.json"
    else:
         in_file = "templates/wf-template-node.json"
    wf_template_json = updateTemplateJsonForUserJson(user_request)

    encoded_wf_template_yaml = generateWorkflowFromJsonTemplate(wf_template_json)

    # Do not change the order of below function calls
    repository_details = generateUserRepository(user_request, gh_token)
    cloneApplicationTemplateToUserRepository(user_request["template_path"], repository_details, gh_token)
    commitWorkFlowFileToUserRepository(user_request, encoded_wf_template_yaml, gh_token)
