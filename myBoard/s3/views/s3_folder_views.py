from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from myBoard.s3.models.s3_bucket_management import S3BucketManagement

from myBoard.s3.utils import *
from myBoard.s3.models.s3_folder_management import S3FolderManagement
from myBoard.s3.serializers.s3_folder_management import S3FolderManagementSerializer
from myBoard.s3.models.s3_file_management import S3FileManagement
from myBoard.s3.serializers.s3_file_management import S3FileManagementSerializer
from myBoard.s3.messages import S3_FOLDER_MESSAGE, S3_MESSAGE, S3_FILE_MESSAGE

from django.core.paginator import Paginator

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
            if folder.count() == 0 or folder_id <= 0:
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

                s3 = s3Utility.connect_s3_resource()
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

        try:
            bucket = S3BucketManagement.objects.get(bucket_name=bucket_name)
        except S3BucketManagement.DoesNotExist as e:
            logger.error({'message': str(e)})
            logger.error({'message': S3_MESSAGE['BUCKET_NAME_NOT_EXIST']})
            return Response({'message': S3_MESSAGE['BUCKET_NAME_NOT_EXIST']}, status=status.HTTP_400_BAD_REQUEST)
        
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
            "bucket_id": bucket.id,
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

            if file.count() == 0 or file_id <= 0:
                logger.error({'message': S3_FILE_MESSAGE['S3_FILE_NOT_EXIST']})
                return Response({'message': S3_FILE_MESSAGE['S3_FILE_NOT_EXIST']}, status=status.HTTP_400_BAD_REQUEST)
            
            file = S3FileManagement.objects.filter(id=file_id).get()
            file_serializer = S3FileManagementSerializer(file)

            try:
                s3 = s3Utility.connect_s3_resource()
                s3.Object(file_serializer.data['bucket_name'], file_serializer.data['file_key']).delete()

                S3FileManagement.objects.filter(file_key=file_serializer.data['file_key']).delete()

                return Response({'message': S3_FILE_MESSAGE['S3_FILE_REMOVE_SUCCESS']}, status=status.HTTP_200_OK)
            except Exception as e:
                logger.error({'message': str(e)})
                logger.error({'message': S3_FILE_MESSAGE['S3_FILE_REMOVE_FAILED']})
                return Response({'message': S3_FILE_MESSAGE['S3_FILE_REMOVE_FAILED']}, status=status.HTTP_400_BAD_REQUEST)

class S3GetListFileByFolder(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get(self, request):
        data = request.GET
        total = 0
        page = 0
        row_per_page = 12
        list_obj_data = []
        list_data = []

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

        # Check folder_key available
        if 'page' not in data or data['page'] == '':
            logger.error({'message': S3_FOLDER_MESSAGE['S3_FILE_PAGE_IS_REQUIRED']})
            return Response({'message': S3_FOLDER_MESSAGE['S3_FILE_PAGE_IS_REQUIRED']}, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                page = int(data['page'])
                if page <= 0:
                    logger.error({'message': S3_FOLDER_MESSAGE['S3_FILE_PAGE_GREATHAN_0']})
                    return Response({'message': S3_FOLDER_MESSAGE['S3_FILE_PAGE_GREATHAN_0']}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                logger.error({'message': str(e)})
                logger.error({'message': S3_FOLDER_MESSAGE['S3_FILE_PAGE_REQUIRE_INT']})
                return Response({'message': S3_FOLDER_MESSAGE['S3_FILE_PAGE_REQUIRE_INT']}, status=status.HTTP_400_BAD_REQUEST)

        # s3 = s3Utility.connect_s3_resource()
        # bucket_name = s3.Bucket(bucket_name)
        get_folder_id = S3FolderManagement.objects.get(folder_key=folder_key)
        get_all_data_by_folder_id = S3FileManagement.objects.filter(folder_id=get_folder_id.id)
        list_all_data_by_folder_id = S3FileManagementSerializer(get_all_data_by_folder_id, many=True)
        for ia in list_all_data_by_folder_id.data:
            list_obj_data.append(ia)

        total = get_all_data_by_folder_id.count()

        for object_summary in list_obj_data:
            item = {
                "id": object_summary["id"],
                "url": s3Utility.get_object_url(object_summary["bucket_name"], object_summary["file_key"])
            }
           
            list_data.append(item)

        p = Paginator(list_data, row_per_page)
        if page > p.num_pages:
            logger.error({'message': S3_FOLDER_MESSAGE['S3_FILE_PAGE_EMPTY_DATA']})
            return Response({'message': S3_FOLDER_MESSAGE['S3_FILE_PAGE_EMPTY_DATA']}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'total': total, 'page': page, 'num_pages': p.num_pages, 'row_per_page': row_per_page, 'data': p.page(page).object_list}, status=status.HTTP_200_OK)

class GetFolderByBucketId(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get(data, request):
        data = request.GET

        # Check bucketname available
        if 'bucket_id' not in data or data['bucket_id'] == '':
            logger.error({'message': S3_MESSAGE['EMPTY_BUCKET_ID']})
            return Response({'message': S3_MESSAGE['EMPTY_BUCKET_ID']}, status=status.HTTP_400_BAD_REQUEST)
        else:
            bucket_id = data['bucket_id']
        
        try:
            folder = S3FolderManagement.objects.filter(bucket_id=bucket_id)
        except S3FolderManagement.DoesNotExist as e:
            logger.error({'message': str(e)})
            logger.error({'message': S3_MESSAGE['BUCKET_ID_NOT_EXISTS']})
            return Response({'message': S3_MESSAGE['BUCKET_ID_NOT_EXISTS']}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error({'message': str(e)})
            logger.error({'message': S3_MESSAGE['BUCKET_ID_NOT_EXISTS']})
            return Response({'message': S3_MESSAGE['BUCKET_ID_NOT_EXISTS']}, status=status.HTTP_400_BAD_REQUEST)
        
        folder_serializer = S3FolderManagementSerializer(folder, many=True)
        list_data = []
        for item in folder_serializer.data:
            image_thumb = S3FileManagement.objects.filter(folder_id=item["id"]).first()
            data = item
            if image_thumb is not None:
                data["image_thumb"] = s3Utility.get_object_url(image_thumb.bucket_name, image_thumb.file_key)
            else: data["image_thumb"] = ""
            list_data.append(data)
        return Response({'data': list_data}, status=status.HTTP_200_OK)

