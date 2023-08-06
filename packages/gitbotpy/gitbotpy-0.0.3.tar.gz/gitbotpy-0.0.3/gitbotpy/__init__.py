import os

class git:
    def list_dir(path):
        l = os.listdir(path)
        l.remove('.git')
        return l
    def push_all_files(disk,path,message):
        os.system(f'cmd /k "{disk}: && cd {path} && git add . && git commit -m "{message}" && git push origin master"')
    def push_one_file(disk,path,filename,message):
        os.system(f'cmd /k "{disk}: && cd {path} && git add {filename} && git commit -m "{message}" && git push origin master"')
    def clone(disk,path,gitlink):
        os.system(f'cmd /k "{disk}: && cd {path} && git clone {gitlink}"')
    def remove_file(disk,path,filename,message):
        os.system(f'cmd /k "{disk}: && cd {path} && git rm {filename} && git commit -m "{message}" && git push origin master"')
    def remove_repo(disk,path,foldername,message):
        os.system(f'cmd /k "{disk}: && cd {path} && git rm -r {foldername} && git commit -m "{message}" && git push origin master"')
    def pull(disk,path):
        os.system(f'cmd /k "{disk}: && cd {path} && git pull"')
    def config(username,email):
        os.system(f'cmd /k "git config --global user.name "{username}" && git config --global user.email "{email}""')
    def status(disk,path):
        os.system(f'cmd /k "{disk}: && cd {path} && git status"')
    def log(disk,path):
        os.system(f'cmd /k "{disk}: && cd {path} && git log"')
    def init(disk,path,filename):
        os.system(f'cmd /k "{disk}: && cd {path} && git init {filename}"')
    def reset(disk,path,commit_id):
        os.system(f'cmd /k "{disk}: && cd {path} && git reset {commid_id}"')
