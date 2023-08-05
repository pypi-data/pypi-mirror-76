#! /usr/bin/env python3
import os
from os.path import getsize
import sys
import fire
import pprint
import time
import sqlite3

from .tools import Tools
from .config import Config
from .progress import ProgressPercentage

        
            
class TowerCrane():
    def __init__(self):
        """
        Make an instance of our cloud, DB, and tools.
        Which we then use in our commands.
        """
        self.project_name = os.path.basename(os.getcwd())
        self.project_dir = os.getcwd() 
        
        self._config  = Config()
        self.db = self._config.get_db_client()
        cloud_client = self._config.get_cloud_client()
        self.tools = Tools(cloud_client=cloud_client,db=self.db)
        
                
    def config(self):
        """
        starting config prompt for setting up the towercrane DB and Cloud
        """
        self._config.config_towercrane()
        
        
    def status(self):
        """
        status of Towercrane for current directory
        """
        self.tools.status(self.project_dir)
        
        
    def scan(self):
        """
        Scan the directory 
        """
        self.tools.scan(self.project_dir)
        
    def init(self):
        """
        Project Initialization: scans the directory and adds the files
        """
        self.tools.init_project(self.project_name,self.project_dir)
        self.tools.scan(self.project_dir)
        self.tools.add(self.project_name,self.project_dir)
        

    def upload(self):   
        """
        Uploading the added files
        """
        queue_files = self.tools.load_queue(self.project_name,status="upload")
        self.tools.upload(self.project_name,self.project_dir,queue_files)
        self.db.change_status_file(queue_files,'uploaded')
        self.db.change_status_file(queue_files,'local_and_cloud')
        #TODO  check with aws if they're uploaded completely
        

    def remove(self):
        """
        Removing the uploaded files from local
        """
        queue_files = self.tools.load_queue(self.project_name,status="local_and_cloud")
        self.db.change_status_file(queue_files,'remove')
        queue_files = self.tools.load_queue(self.project_name,status="remove")
        self.tools.remove(queue_files,self.project_name,self.project_dir)
        self.db.change_status_file(queue_files,"removed")
        self.db.change_status_file(queue_files,'cloud')
        # TODO check if they're removed completely with a os.listdir()
    
    def makepublic(self):
            """
            Make the Project public
            """
            self.tools.make_project_public(self.project_dir,self.project_name)

    
    def download(self):
        """
        Downloading the files from cloud and putting them back where they where
        """
        queue_files = self.tools.load_queue(self.project_name,status="cloud")
        self.db.change_status_file(queue_files,'download')
        queue_files = self.tools.load_queue(self.project_name,status="download")
        self.tools.download(self.project_name,self.project_dir,queue_files)
        self.db.change_status_file(queue_files,'local_and_cloud')



def main():
    if len(sys.argv)>1 and sys.argv[1] == "config":
        Config().config_towercrane()
    else:
        fire.Fire(TowerCrane)
    
 
if __name__ == "__main__":
    main()


    
    
