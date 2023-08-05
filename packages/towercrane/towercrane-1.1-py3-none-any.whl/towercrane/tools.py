import random
import string
import os
from os.path import getsize
import shutil
import errno
import time
import zipfile
from tabulate import tabulate

bucket_name =  "towercrane-projects"

"""
Config tools 

id_generator:  for id generation 
read_config:   reading config file
write_config:  writing config file
"""
def id_generator(length):
    return "".join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

def read_config(project_dir):
    TowercraneConfig = {"project_name":"",
                       "projectkey":"",
                       "publicurl":""}
    with open(os.path.join(project_dir,"towercrane"),"r") as f:
        for line in f.readlines():
            configKey = line.strip().split(":")[0]
            configValue = line.strip().split(":")[1]
            TowercraneConfig[configKey] = configValue
    return TowercraneConfig
    
def write_config(project_dir,TowercraneConfig):
    with open(os.path.join(project_dir,"towercrane"),"w") as f:
            f.write("project_name:"+TowercraneConfig["project_name"]+"\n"+
                    "projectkey:"+TowercraneConfig["projectkey"]+"\n"+
                    "publicurl:"+TowercraneConfig["publicurl"]
                    )








class Tools():
    def __init__(self,cloud_type="aws",cloud_client=None,db=None):
        self.cloud_type = cloud_type
        self.cloud_client = cloud_client
        self.db = db
        
    """
    Local Tools:
    These are the tools for project initialization, scanning files and adding them to DB.
    
    init_project:   initializing project config, and storage in the cloud.
    scan:           scanning local files               
    add:            adding files to DB with local status
    """
    def init_project(self,project_name,project_dir):
        """
        checks if it can find a towercrane file. 
        if not, creates one and creates the project too.
        """
        projectkey = id_generator(10)
        if "towercrane" not in os.listdir(project_dir):
            print(f'Initializing project:"{project_name}" with projectkey: "{projectkey}" ')
            self.TowercraneConfig = {"project_name":project_name,
                                    "projectkey":projectkey,
                                    "publicurl":"private_project"
                                    }
            write_config(project_dir,self.TowercraneConfig)
            project_insert_report = self.db.create_project(project_name,project_dir,projectkey)
            print(project_insert_report)
        
        elif "towercrane" in os.listdir(project_dir):
           self.TowercraneConfig = read_config(project_dir)
           print(f'project:"{self.TowercraneConfig["project_name"]}" with projectkey: "{self.TowercraneConfig["projectkey"]}" Already Exists')
           

        
        
    def scan(self,project_dir):
        """
        Scans the local files and looks for one of the file dtypes.
        And then adds what it finds to a dictionary.
        """
        ftypes = [".csv", ".data", ".xlsx"]
        print("Scanning directory : ",project_dir)
        print("Searching for : ",ftypes)
        self.localfiles = {}
        for dirpath, dirnames, filenames in os.walk(project_dir, topdown=True):
            for filename in filenames:
                for ftype in ftypes:
                    if ftype in filename:
                        self.localfiles[filename] = {
                            "filename": filename,
                            "filesize": getsize(os.path.join(dirpath, filename)),
                            "abspath": os.path.join(dirpath, filename),
                            "dirpath": dirpath,
                            
                        }
        print("Found These: ",[file_name for file_name in self.localfiles.keys()])    
    
    def add(self,project_name,project_dir):
        if self.localfiles:
            for k,file_meta in self.localfiles.items():
                filekey = id_generator(20)
                projectkey = self.TowercraneConfig["projectkey"]
                file_insert_report = self.db.create_file(file_meta,project_name,filekey,projectkey)
                print(file_insert_report)

    
    """
    Queue Tools:
    These are the tools for running tasks on a loaded queue.
    
    load_queue: loads a queue using a status and db tools
    upload:     loads a queue of fiels with upload status
    
    """
    def load_queue(self,project_name,status):
        files_with_status = self.db.get_files_with_status(project_name,status)
        return files_with_status


    def _zip(self,object_name,project_dir,filekey_abspaths):
        os.chdir(project_dir)
        zipObj = zipfile.ZipFile(object_name,"w")
        for filekey,abspath in filekey_abspaths:
            print("added to zip: ",filekey, "  ",abspath)
            zipObj.write(abspath,arcname=f"{filekey}_" +os.path.basename(abspath)+".original")
        zipObj.close()
    
    
    def upload(self,project_name,project_dir,queue_files):
        object_name = project_name+"-project-towercrane-files.zip"
        zippath = os.path.join(project_dir,object_name)
        if object_name in os.listdir(project_dir):
            os.remove(os.path.join(project_dir,object_name))    
        
        filekey_abspaths = [(f[0],f[3]) for f in queue_files]
        self._zip(object_name,project_dir,filekey_abspaths)
        print("Uploading zip: ",zippath)
        self.cloud_client.upload_file(bucket_name,zippath,object_name)
        

    
    def make_project_public(self,project_dir,project_name):
        object_name = project_name+"-project-towercrane-files.zip"
        # get public url of zip file, and then read and write the public url to towercrane file
        publicurl = self.cloud_client.get_public_url(bucket_name,object_name)
        self.TowercraneConfig = read_config(project_dir)
        self.TowercraneConfig["publicurl"] = publicurl 
        write_config(project_dir,self.TowercraneConfig)
        
            
        
    
    
    def remove(self,queue_files,project_name,project_dir):
        filekey_abspaths = [(f[0],f[3]) for f in queue_files]
        print(filekey_abspaths)
        for filekey,abspath in filekey_abspaths:
            try:
                
                os.remove(abspath)
                os.system(f"touch {os.path.dirname(abspath)}/{filekey}_{os.path.basename(abspath)}.towercrane")
                print("removed :"+ abspath)
                time.sleep(0.5)
                
            except OSError as e: 
                if e.errno == errno.ENOENT: # errno.ENOENT = no such file or directory
                    print("no such file to remove")
                else:
                    raise 
        zipfile_name = project_name+"-project-towercrane-files.zip"
        if zipfile_name in os.listdir(project_dir):
             os.remove(os.path.join(project_dir,zipfile_name))
        
    
    
    def download(self,project_name,project_dir,queue_files):
        object_name = project_name+"-project-towercrane-files.zip"
        print(f"Downloading {object_name} from Bucket \"{bucket_name}\"")
        self.cloud_client.download_file(bucket_name,object_name,project_dir)
    
        #distribute the files to their original spots
        unzip_dir = f"{project_name}_towercrane_unzip"
        if unzip_dir in os.listdir(project_dir):
            shutil.rmtree(os.path.join(project_dir,unzip_dir))
            print("removed :",unzip_dir)
        
        zippath = os.path.join(project_dir,object_name)
        with zipfile.ZipFile(zippath , 'r') as zipObj:
            os.chdir(project_dir)
            os.mkdir(unzip_dir)
            zipObj.extractall(unzip_dir)
    
        
        """
        It walks in the whole project directory and finds .towercrane files and replaces them with the files with same filekey 
        which were extracted from the zip file.
        """
        os.chdir(project_dir)
        os.walk(project_dir)
        for dirpath, dirnames, filenames in os.walk(project_dir, topdown=True):
            for filename in filenames:
                if ".towercrane" in filename:
                    filekey = filename.split("_")[0]
                    original_filename = "".join(filename.strip(".towercrane").split("_")[1:])
                    for zip_file in os.listdir(unzip_dir):
                        if filekey in zip_file:
                            print(f"cp {os.path.join(project_dir,unzip_dir,zip_file)}  {os.path.join(dirpath,original_filename)}")
                            os.system(f"cp {os.path.join(project_dir,unzip_dir,zip_file)}  {os.path.join(dirpath,original_filename)}")
                            os.remove(os.path.join(dirpath,filename))
        
        shutil.rmtree(os.path.join(project_dir,unzip_dir))
        os.remove(os.path.join(project_dir,object_name))
            
    
    def status(self,project_dir):
        """
        if towercrane file exists, gets the project and its files from db 
        and pretty prints them
        """
        
        if "towercrane" not in os.listdir(project_dir):
            print('(!) No project has been initialized yet.\n => you can use "towercrane init" to start a new project.\n => Or it might be because you have lost the "towercrane config file" ')
        
        elif "towercrane" in os.listdir(project_dir):
            TowercraneConfig = read_config(project_dir)
            project, files = self.db.get_project(TowercraneConfig["projectkey"])
            files_table = tabulate([[file[1],file[0],file[2],file[-1]] for file in files], headers=['File Name', 'File Key','Size','status'], tablefmt='orgtbl')
            print(f'project:"{TowercraneConfig["project_name"]}" with projectkey: "{TowercraneConfig["projectkey"]}"\nFiles added to the project: \n\n{files_table}')
            
            


 
        
        
        