from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from myBoard.s3.utils import *
from myBoard.s3.messages import S3_MESSAGE



import boto3
import os

import logging

logger = logging.getLogger(__name__)


class S3ApiView(APIView):
  permission_classes = (IsAuthenticated,)   

  def post(self, request):
        data = request.data

        # Check bucketname available
        if 'bucket_name' not in data or data['bucket_name'] == '':
            logger.error({'message': S3_MESSAGE['EMPTY_BUCKET_NAME']})
            return Response({'message': S3_MESSAGE['EMPTY_BUCKET_NAME']}, status=status.HTTP_400_BAD_REQUEST)
        else:
            bucket_name = data['bucket_name']


        try:
            s3_client = s3Utility.connect_s3()
            print(s3_client)
            s3_client.create_bucket(Bucket=bucket_name)
        except Exception as e:
            logger.error(str(e))
            logger.error({'message': S3_MESSAGE['CREATE_BUCKET_NAME_FAILED']})
            return Response({'message': S3_MESSAGE['CREATE_BUCKET_NAME_FAILED']}, status=status.HTTP_400_BAD_REQUEST)
        return Response({})
