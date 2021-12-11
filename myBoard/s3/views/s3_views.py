from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser, MultiPartParser
from django.core.files.storage import FileSystemStorage
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status

from myBoard.s3.utils import *
from myBoard.s3.models.s3_bucket_management import S3BucketManagement
from myBoard.s3.models.s3_file_management import S3FileManagement
from myBoard.s3.messages import S3_MESSAGE, S3_FOLDER_MESSAGE
from myBoard.settings import S3_TEMP_FOLDER

import logging
import os
import boto3
import json

logger = logging.getLogger(__name__)


class S3Bucket(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)   

    def post(self, request):
        data = request.data

        # Check bucketname available
        if 'bucket_name' not in data or data['bucket_name'] == '':
            logger.error({'message': S3_MESSAGE['EMPTY_BUCKET_NAME']})
            return Response({'message': S3_MESSAGE['EMPTY_BUCKET_NAME']}, status=status.HTTP_400_BAD_REQUEST)
        else:
            bucket_name = data['bucket_name']

        # Get list buckets
        list_buckets = s3Utility.get_list_buckets()

        # Check bucket_name exists in list
        if bucket_name in list_buckets:
            return Response({'message': S3_MESSAGE['BUCKET_NAME_EXISTS']}, status=status.HTTP_400_BAD_REQUEST)

        # Create list bucket
        create_bucket = s3Utility.create_bucket(bucket_name)
        if create_bucket['status'] == 1:
            return Response({'message': S3_MESSAGE['CREATE_BUCKET_NAME_FAILED']}, status=status.HTTP_400_BAD_REQUEST)
        
        # Save bucket to DB
        bucket = {
            "bucket_name": bucket_name,
            "bucket_region": os.environ["MYBOARD_REGION"],
            "created_by": request.user.username,
            "updated_by": request.user.username,
            "status": 0
        }
        S3BucketManagement.objects.create(**bucket)

        return Response({'message': S3_MESSAGE['CREATE_BUCKET_NAME_SUCCESS']}, status=status.HTTP_200_OK)

    def delete(self, request):
        data = request.data

        # Check bucketname available
        if 'bucket_name' not in data or data['bucket_name'] == '':
            logger.error({'message': S3_MESSAGE['EMPTY_BUCKET_NAME']})
            return Response({'message': S3_MESSAGE['EMPTY_BUCKET_NAME']}, status=status.HTTP_400_BAD_REQUEST)
        else:
            bucket_name = data['bucket_name']

        s3 = boto3.resource('s3',
            aws_access_key_id=os.environ['MYBOARD_AWS_S3_ACCESS_KEY_ID'],
            aws_secret_access_key= os.environ['MYBOARD_AWS_S3_SECRET_ACCESS_KEY']
        )
        bucket = s3.Bucket(bucket_name)
        try:
            for key in bucket.objects.all():
                key.delete()
            bucket.delete()
            S3BucketManagement.objects.filter(bucket_name=bucket_name).delete()
            return Response({'message': S3_MESSAGE['DELETE_BUCKET_SUCCESS']}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error({'message': str(e)})
            logger.error({'message': S3_MESSAGE['DELETE_BUCKET_FAILED']})
            return Response({'message': S3_MESSAGE['DELETE_BUCKET_FAILED']}, status=status.HTTP_400_BAD_REQUEST)

class GetS3Object(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def post(self, request):
        data = request.data

        # Check bucketname available
        if 'bucket_name' not in data or data['bucket_name'] == '':
            logger.error({'message': S3_MESSAGE['EMPTY_BUCKET_NAME']})
            return Response({'message': S3_MESSAGE['EMPTY_BUCKET_NAME']}, status=status.HTTP_400_BAD_REQUEST)
        else:
            bucket_name = data['bucket_name']
        
        # Check bucketname available
        if 'key_name' not in data or data['key_name'] == '':
            logger.error({'message': S3_MESSAGE['EMPTY_KEY_NAME']})
            return Response({'message': S3_MESSAGE['EMPTY_KEY_NAME']}, status=status.HTTP_400_BAD_REQUEST)
        else:
            key_name = data['key_name']

        url = s3Utility.get_object_url(bucket_name, key_name)
        return Response({'url': url}, status=status.HTTP_200_OK)

class SetS3BucketPublicAccess(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def post(self, request):
        data = request.data

        # Check bucketname available
        if 'bucket_name' not in data or data['bucket_name'] == '':
            logger.error({'message': S3_MESSAGE['EMPTY_BUCKET_NAME']})
            return Response({'message': S3_MESSAGE['EMPTY_BUCKET_NAME']}, status=status.HTTP_400_BAD_REQUEST)
        else:
            bucket_name = data['bucket_name']
        statement = []
        statment_public = {
            'Effect': 'Allow',
            'Principal': '*',
            'Action': ['s3:*'],
            'Resource': f'arn:aws:s3:::{bucket_name}/*'
        }
        statement.append(statment_public)
        statment_list_object = {
            'Effect': 'Allow',
            'Principal': '*',
            'Action': ['s3:List*', 's3:DeleteBucket', 's3:PutObject', 's3:PutObjectAcl'],
            'Resource': [
                f'arn:aws:s3:::{bucket_name}',
                f'arn:aws:s3:::{bucket_name}/*'
            ]
        }
        statement.append(statment_list_object)
        bucket_policy = {
            'Version': '2012-10-17',
            'Statement': statement
        }

        try:
            bucket_policy = json.dumps(bucket_policy)
            s3_client = s3Utility.connect_s3()
            s3_client.put_bucket_policy(Bucket=bucket_name, Policy=bucket_policy)
            return Response({'message': S3_MESSAGE['SET_POLICY_BUCKET_PUBLIC_SUCCESS']}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error({'message': str(e)})
            logger.error({'message': S3_MESSAGE['SET_POLICY_BUCKET_PUBLIC_FAILED']})
            return Response({'message': S3_MESSAGE['SET_POLICY_BUCKET_PUBLIC_FAILED']}, status=status.HTTP_400_BAD_REQUEST)

class S3UploadSingle(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)
    parser_class = (FileUploadParser,)

    def post(self, request):
        data = request.data

        # Check bucketname available
        if 'bucket_name' not in data or data['bucket_name'] == '':
            logger.error({'message': S3_MESSAGE['EMPTY_BUCKET_NAME']})
            return Response({'message': S3_MESSAGE['EMPTY_BUCKET_NAME']}, status=status.HTTP_400_BAD_REQUEST)
        else:
            bucket_name = data['bucket_name']
        
        # Check folder_key available
        if 'folder_key' not in data or data['folder_key'] == '':
            logger.error({'message': S3_FOLDER_MESSAGE['EMPTY_S3_FOLDER_KEY']})
            return Response({'message': S3_FOLDER_MESSAGE['EMPTY_S3_FOLDER_KEY']}, status=status.HTTP_400_BAD_REQUEST)
        else:
            folder_key = data['folder_key']

        if 'file' not in request.FILES:
            logger.error({'message': S3_FOLDER_MESSAGE['S3_FILE_UPLOAD_NOT_FOUND']})
            return Response({'message': S3_FOLDER_MESSAGE['S3_FILE_UPLOAD_NOT_FOUND']}, status=status.HTTP_400_BAD_REQUEST)
        else:
            img_file = request.FILES['file']


        file_name, file_ext = os.path.splitext(img_file.name)
        if file_ext not in ['.jpg', '.png', '.jpeg', '.mp4', 'mov']:
            logger.error({'message': S3_FOLDER_MESSAGE['S3_FILE_UPLOAD_UNVALID_EXT']})
            return Response({'message': S3_FOLDER_MESSAGE['S3_FILE_UPLOAD_UNVALID_EXT']}, status=status.HTTP_400_BAD_REQUEST)

        s3_client = s3Utility.connect_s3()
        fs = FileSystemStorage()
        filename = fs.save(f'{S3_TEMP_FOLDER}{img_file.name}', img_file)
        uploaded_file_path = fs.path(filename)

        try:
            s3_client.upload_file(uploaded_file_path, bucket_name, f'{folder_key}/{img_file.name}', ExtraArgs={'ACL': 'public-read'})
            uploaded_data = {
                "file_name": img_file.name,
                "file_key": f'{folder_key}/{img_file.name}',
                "bucket_name": bucket_name,
                "created_by": request.user.username,
                "updated_by": request.user.username
            }
            S3FileManagement.objects.create(**uploaded_data)
        except Exception as e:
            logger.error({'message': S3_FOLDER_MESSAGE['S3_FILE_UPLOAD_FAILED']})
            return Response({'message': S3_FOLDER_MESSAGE['S3_FILE_UPLOAD_FAILED']}, status=status.HTTP_400_BAD_REQUEST)

        # Remove temp file
        fs.delete(uploaded_file_path)
        return Response({'message': S3_FOLDER_MESSAGE['S3_FILE_UPLOAD_SUCCESS']}, status=status.HTTP_200_OK)

class S3UploadMultiple(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def post(self, request):
        data = request.data
        print(data)
        # Check bucketname available
        if 'bucket_name' not in data or data['bucket_name'] == '':
            logger.error({'message': S3_MESSAGE['EMPTY_BUCKET_NAME']})
            return Response({'message': S3_MESSAGE['EMPTY_BUCKET_NAME']}, status=status.HTTP_400_BAD_REQUEST)
        else:
            bucket_name = data['bucket_name']
        
        # Check folder_key available
        if 'folder_key' not in data or data['folder_key'] == '':
            logger.error({'message': S3_FOLDER_MESSAGE['EMPTY_S3_FOLDER_KEY']})
            return Response({'message': S3_FOLDER_MESSAGE['EMPTY_S3_FOLDER_KEY']}, status=status.HTTP_400_BAD_REQUEST)
        else:
            folder_key = data['folder_key']

        if 'files' not in request.FILES:
            logger.error({'message': S3_FOLDER_MESSAGE['S3_FILE_UPLOAD_NOT_FOUND']})
            return Response({'message': S3_FOLDER_MESSAGE['S3_FILE_UPLOAD_NOT_FOUND']}, status=status.HTTP_400_BAD_REQUEST)
        else:
            img_files = request.FILES['files']

        logger.info({"A": request.FILES.get('files')})
        return Response({'message': S3_FOLDER_MESSAGE['S3_FILE_UPLOAD_SUCCESS']}, status=status.HTTP_200_OK)