print("Hello from the creator of AutoGit, Saran,Abhilash,Abhiraman,Tarun.Kindly do report bug if any.This message will not be shown again.:)")

import os
class AutoGitUtils():
    
        
    def display(disk,path,msg,folder,link):
        print(disk,path,msg,folder,link)

  
         
        
    def clone(disk,path,gitlink):
        os.system(f'cmd /k "{disk}: && cd {path} && git clone {gitlink} && git status "')


    def push_pull(disk,path,msg):
        os.system(f'cmd /k " {disk}: && cd {path} && git pull  && git add . && git commit -m """{msg}""" && git push origin master && git status"')



    def del_folder_subfol(disk,path,folder,msg):
        os.system(f'cmd /k " {disk}: && cd {self.path} &&git rm -r {folder} && git commit -m "{msg}" && git push origin master && git status"')
