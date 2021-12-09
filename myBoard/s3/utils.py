import os
import boto3

class s3Utility:
    @staticmethod
    def connect_s3():
        return boto3.client('s3',  aws_access_key_id=os.environ["MYBOARD_AWS_S3_ACCESS_KEY_ID"],
            aws_secret_access_key=os.environ["MYBOARD_AWS_S3_SECRET_ACCESS_KEY"])