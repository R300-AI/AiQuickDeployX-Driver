from git import Repo

class Module_Installer():
    def __init__(self):
        pass
    
    def install_from_url(self, git_url, local_path):
        Repo.clone_from(git_url, local_path)