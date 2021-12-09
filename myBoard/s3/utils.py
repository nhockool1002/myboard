from rest_framework import status
from myBoard.s3.messages import S3_MESSAGE

import os
import boto3
import urllib

import logging

logger = logging.getLogger(__name__)
class s3Utility:
    @staticmethod
    def connect_s3():
        return get_client()
    
    @staticmethod
    def get_list_buckets():
        s3_client = get_client()
        response_list_buckets = s3_client.list_buckets()
        list_buckets = []
        for item in response_list_buckets["Buckets"]:
            list_buckets.append(item["Name"])
        return list_buckets
    
    @staticmethod
    def create_bucket(bucket_name):
        s3_client = get_client()
        try:
            s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': os.environ["MYBOARD_REGION"]})
            # Put public access
            return {"status": 0}
        except Exception as e:
            logger.error({'message': str(e)})
            return {"status": 1}
    
    @staticmethod
    def get_object_url(bucket_name, key_name):
        s3_client = get_client()
        location = s3_client.get_bucket_location(Bucket=bucket_name)['LocationConstraint']
        return f"https://%s.s3.%s.amazonaws.com/%s" % (bucket_name, location, urllib.parse.quote(key_name, safe="~()*!.'"))

def get_client():
    return boto3.client('s3',  aws_access_key_id=os.environ["MYBOARD_AWS_S3_ACCESS_KEY_ID"],
            aws_secret_access_key=os.environ["MYBOARD_AWS_S3_SECRET_ACCESS_KEY"])