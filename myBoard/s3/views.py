from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from myBoard.s3.utils import *
from myBoard.s3.messages import S3_MESSAGE

import logging
import os
import boto3

logger = logging.getLogger(__name__)


class CreateS3Bucket(APIView):
    permission_classes = (IsAuthenticated,)   

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
            return Response({'message': S3_MESSAGE['CREATE_BUCKET_NAME_SUCCESS']}, status=status.HTTP_200_OK)

class GetS3Object(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        data = request.data
        url = s3Utility.get_object_url(data["bucket_name"], data["key_name"])
        return Response({'url': url}, status=status.HTTP_200_OK)