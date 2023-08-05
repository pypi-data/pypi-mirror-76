import logging
import os
import boto3
from botocore.exceptions import ClientError
from google.cloud import storage
from .progress import ProgressPercentage
from os.path import getsize
import sys


"""
########################################
############## AWS S3 ##################
########################################
"""
class S3():
    """
    Cloud Tools:
    These are the tools for working with cloud    
    """
    
    def __init__(self,region="us-east-1"):
        try:
            self.s3_client = boto3.client('s3', region_name=region)
            self.s3_res = boto3.resource('s3')
            self.s3_client.list_buckets() # making sure the client is working properly
            
        except ClientError as e:
            if e.response['Error']['Code'] == 'ExpiredToken':
                sys.exit("Cannot connect to AWS S3 client. AWS Token is expired.")                   

    def list_buckets(self):
        response = self.s3_client.list_buckets()
        buckets = response['Buckets']
        return buckets

    def list_objects(self, bucket_name):
        mybucket = self.s3_res.Bucket(bucket_name)
        all_objects = []
        for object_summary in mybucket.objects.all() :
            all_objects.append(object_summary.key)
        return all_objects
        
        
    def get_public_url(self,bucket_name,object_name):
        # response = self.s3_client.get_bucket_location(Bucket=bucket_name)
        # bucket_location = response['LocationConstraint'] if response['LocationConstraint'] else "us-east-1"
        
        self.s3_client.put_object_acl(ACL="public-read",Bucket=bucket_name,Key=object_name)        
        object_url = f"https://{bucket_name}.s3.amazonaws.com/{object_name}" # whats the pattern for other regions? TODO
        return object_url
        
        
    def create_bucket(self,bucket_name):
        try:
            if self.region is None or self.region == "us-east-1":
                self.s3_res.create_bucket(Bucket=bucket_name)
            else:
                location = {'LocationConstraint': self.region}
                self.s3_res.create_bucket(Bucket=bucket_name,
                                        CreateBucketConfiguration=location)
        except ClientError as e:
            logging.error(e)
            return False
        return True
    
    
    def upload_file(self,bucket_name,abspath,object_name):
        try:
            with open(abspath, "rb") as f:
                response = self.s3_client.upload_fileobj(f,bucket_name, object_name,
                                                         Callback=ProgressPercentage(object_name,size=float(getsize(abspath)))
                                                            )            
                return True, response
            
        except ClientError as e:
            logging.error(e)
            return False
        
    
    
    def download_file(self,bucket_name,object_name,project_dir):
        try:
            file_size = self.s3_client.head_object(
                                            Bucket=bucket_name,
                                            Key=object_name
                                            )['ContentLength']
        
            with open(os.path.join(project_dir,object_name), 'wb') as f:
                response = self.s3_client.download_fileobj(bucket_name, object_name, f,
                                                           Callback=ProgressPercentage(object_name,float(file_size))
                                                           )
                                                          
        except ClientError as e:
            logging.error(e)
            return False
        return True
    
    

    def list_cloud_projects(self):
        buckets_names = []
        buckets = self.list_buckets()
        for bucket in buckets :
            buckets_names.append(bucket["Name"])
        return buckets_names
    
    def create_cloud_project(self,project_name):
        bucket_name = project_name
        self.create_bucket(bucket_name)






"""
########################################
######### Google Cloud Storage #########
########################################
"""

class GS():
    """
    Cloud Tools:
    These are the tools for working with cloud    
    """
    
    def __init__(self):
        try:
            self.gs_client = storage.Client()
            self.gs_client.list_buckets() 
            
        except ClientError as e:
            if e.response['Error']['Code'] == 'ExpiredToken':
                sys.exit("Cannot connect to GCP storage client. Token is expired.")                   

    def list_buckets(self):
        buckets_iterator = self.gs_client.list_buckets()
        buckets = [b.name for b in buckets_iterator ]
        return buckets

    def list_objects(self, bucket_name):
        bucket_objects_iterator = self.gs_client.list_blobs(bucket_name)
        bucket_objects = [o.name for o in bucket_objects_iterator]
        return bucket_objects
        
        
    def get_public_url(self,bucket_name,object_name):
        bucket = self.gs_client.bucket(bucket_name)
        blob = bucket.blob(object_name)
        blob.make_public()
        return  blob.public_url
        
        
    def create_bucket(self,bucket_name):
        try:
            self.gs_client.create_bucket(bucket_name)    
        except ClientError as e:
            logging.error(e)
            return False
        return True
    
    
    def upload_file(self,bucket_name,abspath,object_name):
        try:
            bucket = self.gs_client.bucket(bucket_name)
            blob = bucket.blob(object_name)
            blob.upload_from_filename(abspath)
            
        except ClientError as e:
            logging.error(e)
        
    
    
    def download_file(self,bucket_name,object_name,project_dir):
        try:
            bucket = self.gs_client.bucket(bucket_name)
            blob = bucket.blob(object_name)
            blob.download_to_filename(os.path.join(project_dir,object_name))                                              
        
        except ClientError as e:
            logging.error(e)
            
    
    def list_cloud_projects(self):
        buckets = self.list_buckets()
        return buckets
    
    def create_cloud_project(self,project_name):
        bucket_name = project_name
        self.create_bucket(bucket_name)


