import sys
from git.repo import Repo
import os
import sys
import ast
from datetime import datetime

local_repo_path  = "user/repository/"+str(datetime.now(tz=None))
def cloneApplicationTemplateToUserRepository(app_template: any, repository_details: dict, user_token: any)->None:
    
    repository = Repo.clone_from('https://'+repository_details['owner']['login']+':'+user_token+'@'+app_template.split("//",1)[1], local_repo_path)
    os.chdir(local_repo_path)
    repository.create_remote('userorigin', 'https://'+repository_details['owner']['login']+':'+user_token+'@github.com/'+repository_details['full_name']+'.git')
    response = repository.remotes.userorigin.push('master:master')
    print("Template successfully cloned to user repository ", response)


if __name__ == '__main__':
    app_template = sys.argv[1]
    repository_details =  sys.argv[2]
    user_token = sys.argv[3]
    json_acceptable_string = repository_details.replace("'", "\"")
    repository_details = ast.literal_eval(json_acceptable_string)
    cloneApplicationTemplateToUserRepository(app_template, repository_details, user_token)
