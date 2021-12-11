from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status

from myBoard.s3.utils import *
from myBoard.s3.models.s3_folder_management import S3FolderManagement
from myBoard.s3.serializers.s3_folder_management import S3FolderManagementSerializer
from myBoard.s3.models.s3_file_management import S3FileManagement
from myBoard.s3.serializers.s3_file_management import S3FileManagementSerializer
from myBoard.s3.messages import S3_FOLDER_MESSAGE, S3_MESSAGE, S3_FILE_MESSAGE

import re
import os
import logging

logger = logging.getLogger(__name__)

class S3Folder(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get(self, request):
        folder_id = ''
        data_query = ''
        data_query_serializer = ''

        if 'folder_id' not in request.GET or request.GET['folder_id'] == '':
            data_query = S3FolderManagement.objects.all()
            data_query_serializer = S3FolderManagementSerializer(data_query, many=True)
            return Response({"data": data_query_serializer.data}, status=status.HTTP_200_OK)
        else:
            try:
                folder_id = int(request.GET['folder_id'])
            except Exception as e:
                logger.error({'message': str(e)})
                logger.error({'message': S3_FOLDER_MESSAGE['S3_FOLDER_ID_REQUIRE_INT']})
                return Response({'message': S3_FOLDER_MESSAGE['S3_FOLDER_ID_REQUIRE_INT']}, status=status.HTTP_400_BAD_REQUEST)

            if isinstance(folder_id, int) and folder_id > 0:
                data_query = S3FolderManagement.objects.get(id=folder_id)
                data_query_serializer = S3FolderManagementSerializer(data_query)
                return Response({"data": [data_query_serializer.data]}, status=status.HTTP_200_OK)
            else:
                logger.error({'message': S3_FOLDER_MESSAGE['S3_FOLDER_ID_REQUIRE_INT']})
                return Response({'message': S3_FOLDER_MESSAGE['S3_FOLDER_ID_REQUIRE_INT']}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        data = request.GET

        if 'folder_id' not in data or data['folder_id'] == '':
            logger.error({'message': S3_FOLDER_MESSAGE['S3_FOLDER_ID_EMPTY']})
            return Response({'message': S3_FOLDER_MESSAGE['S3_FOLDER_ID_EMPTY']}, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                folder_id = int(request.GET['folder_id'])
            except Exception as e:
                logger.error({'message': str(e)})
                logger.error({'message': S3_FOLDER_MESSAGE['S3_FOLDER_ID_REQUIRE_INT']})
                return Response({'message': S3_FOLDER_MESSAGE['S3_FOLDER_ID_REQUIRE_INT']}, status=status.HTTP_400_BAD_REQUEST)
            
            folder = S3FolderManagement.objects.filter(id=folder_id)
            if folder.count() == 0 or folder_id < 0:
                logger.error({'message': S3_FOLDER_MESSAGE['S3_FOLDER_NOT_EXIST']})
                return Response({'message': S3_FOLDER_MESSAGE['S3_FOLDER_NOT_EXIST']}, status=status.HTTP_400_BAD_REQUEST)
            
            folder = S3FolderManagement.objects.filter(id=folder_id).get()
            folder_serializer = S3FolderManagementSerializer(folder)
            s3_client = s3Utility.connect_s3()
            try:
                response = s3_client.list_objects_v2(Bucket=f'{folder_serializer.data["bucket_name"]}', Prefix=f'{folder_serializer.data["folder_key"]}/')

                if 'Contents' in response:
                    for object in response['Contents']:
                        s3_client.delete_object(Bucket=f'{folder_serializer.data["bucket_name"]}', Key=object['Key'])

                s3 = boto3.resource('s3',
                    aws_access_key_id=os.environ['MYBOARD_AWS_S3_ACCESS_KEY_ID'],
                    aws_secret_access_key= os.environ['MYBOARD_AWS_S3_SECRET_ACCESS_KEY']
                )
                bucket = s3.Bucket(f'{folder_serializer.data["bucket_name"]}')
                bucket.objects.filter(Prefix=f'{folder_serializer.data["folder_key"]}/').delete()

                S3FolderManagement.objects.filter(bucket_name=folder_serializer.data["bucket_name"], folder_key=folder_serializer.data["folder_key"]).delete()

                return Response({'message': S3_FOLDER_MESSAGE['S3_FOLDER_REMOVE_SUCCESS']}, status=status.HTTP_200_OK)
            except Exception as e:
                logger.error({'message': str(e)})
                logger.error({'message': S3_FOLDER_MESSAGE['S3_FOLDER_REMOVE_FAILED']})
                return Response({'message': S3_FOLDER_MESSAGE['S3_FOLDER_REMOVE_FAILED']}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        data = request.data

        if 'folder_name' not in data or data['folder_name'] == '':
            logger.error({'message': S3_FOLDER_MESSAGE['EMPTY_S3_FOLDER_NAME']})
            return Response({'message': S3_FOLDER_MESSAGE['EMPTY_S3_FOLDER_NAME']}, status=status.HTTP_400_BAD_REQUEST)
        else:
            folder_name = data['folder_name']
        
        if 'folder_key' not in data or data['folder_key'] == '':
            logger.error({'message': S3_FOLDER_MESSAGE['EMPTY_S3_FOLDER_KEY']})
            return Response({'message': S3_FOLDER_MESSAGE['EMPTY_S3_FOLDER_KEY']}, status=status.HTTP_400_BAD_REQUEST)
        else:
            folder_key = data['folder_key']

        # Check bucketname available
        if 'bucket_name' not in data or data['bucket_name'] == '':
            logger.error({'message': S3_MESSAGE['EMPTY_BUCKET_NAME']})
            return Response({'message': S3_MESSAGE['EMPTY_BUCKET_NAME']}, status=status.HTTP_400_BAD_REQUEST)
        else:
            bucket_name = data['bucket_name']

        
        special_char = re.compile('[@_!#$%^&*()<>?/\|}{~:]')

        # check string contains special characters or not
        if special_char.search(folder_key) == None:
            folder_key = folder_key.replace(" ", "")

            # Check folder_key exists
            exists = S3FolderManagement.objects.filter(folder_key=folder_key).count()
            if exists > 0:
                logger.error({'message': S3_FOLDER_MESSAGE['S3_FOLDER_KEY_EXISTS']})
                return Response({'message': S3_FOLDER_MESSAGE['S3_FOLDER_KEY_EXISTS']}, status=status.HTTP_400_BAD_REQUEST)
        else:
            logger.error({'message': S3_FOLDER_MESSAGE['S3_FOLDER_KEY_CONTAINS_SPECIAL_CHAR']})
            return Response({'message': S3_FOLDER_MESSAGE['S3_FOLDER_KEY_CONTAINS_SPECIAL_CHAR']}, status=status.HTTP_400_BAD_REQUEST)
        
        # Get list buckets
        list_buckets = s3Utility.get_list_buckets()

        # Check bucket_name exists in list
        if bucket_name not in list_buckets:
            return Response({'message': S3_MESSAGE['BUCKET_NAME_NOT_EXIST']}, status=status.HTTP_400_BAD_REQUEST)
        
        folder_data = {
            "folder_name": folder_name,
            "folder_key": folder_key,
            "bucket_name": bucket_name,
            "created_by": request.user.username,
            "updated_by": request.user.username,
        }

        try:
            S3FolderManagement.objects.create(**folder_data)
            return Response({'message': S3_FOLDER_MESSAGE['S3_FOLDER_CREATE_SUCCESS']}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error({'message': str(e)})
            logger.error({'message': S3_FOLDER_MESSAGE['S3_FOLDER_CREATE_FAILED']})
            return Response({'message': S3_FOLDER_MESSAGE['S3_FOLDER_CREATE_FAILED']}, status=status.HTTP_400_BAD_REQUEST)

class S3File(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def delete(self, request):
        data = request.GET

        if 'file_id' not in data or data['file_id'] == '':
            logger.error({'message': S3_FILE_MESSAGE['S3_FILE_ID_NOT_FOUND']})
            return Response({'message': S3_FILE_MESSAGE['S3_FILE_ID_NOT_FOUND']}, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                file_id = int(request.GET['file_id'])
            except Exception as e:
                logger.error({'message': str(e)})
                logger.error({'message': S3_FILE_MESSAGE['S3_FILE_ID_REQUIRE_INT']})
                return Response({'message': S3_FILE_MESSAGE['S3_FILE_ID_REQUIRE_INT']}, status=status.HTTP_400_BAD_REQUEST)
            
            file = S3FileManagement.objects.filter(id=file_id)

            if file.count() == 0 or file_id < 0:
                logger.error({'message': S3_FILE_MESSAGE['S3_FILE_NOT_EXIST']})
                return Response({'message': S3_FILE_MESSAGE['S3_FILE_NOT_EXIST']}, status=status.HTTP_400_BAD_REQUEST)
            
            file = S3FileManagement.objects.filter(id=file_id).get()
            file_serializer = S3FileManagementSerializer(file)

            try:
                s3 = boto3.resource('s3',
                    aws_access_key_id=os.environ['MYBOARD_AWS_S3_ACCESS_KEY_ID'],
                    aws_secret_access_key= os.environ['MYBOARD_AWS_S3_SECRET_ACCESS_KEY']
                )
                s3.Object(file_serializer.data['bucket_name'], file_serializer.data['file_key']).delete()

                S3FileManagement.objects.filter(file_key=file_serializer.data['file_key']).delete()

                return Response({'message': S3_FILE_MESSAGE['S3_FILE_REMOVE_SUCCESS']}, status=status.HTTP_200_OK)
            except Exception as e:
                logger.error({'message': str(e)})
                logger.error({'message': S3_FILE_MESSAGE['S3_FILE_REMOVE_FAILED']})
                return Response({'message': S3_FILE_MESSAGE['S3_FILE_REMOVE_FAILED']}, status=status.HTTP_400_BAD_REQUEST)
