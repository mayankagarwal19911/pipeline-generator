from git.repo import Repo
import os
from datetime import datetime

local_repo_path  = "user/repository/"+str(datetime.now(tz=None))
def cloneApplicationTemplateToUserRepository(app_template_path: any, repository_details: dict, user_token: any)->None:
    try:
        app_template_path = 'https://'+repository_details['owner']['login']+':'+user_token+'@'+app_template_path.split("//",1)[1]
        repository = Repo.clone_from(app_template_path, local_repo_path)
        os.chdir(local_repo_path)
        user_repo_path = 'https://'+repository_details['owner']['login']+':'+user_token+'@github.com/'+repository_details['full_name']+'.git'
        repository.create_remote('userorigin', user_repo_path)
        response = repository.remotes.userorigin.push('master:master')
        print("Template successfully cloned to user repository ", response)
    except Exception as e:
        print("Failed to clone template to user repository. ", str(e))
