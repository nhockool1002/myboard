from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from myBoard.s3.utils import *
from myBoard.s3.messages import S3_MESSAGE

import logging
import os
import boto3
import json

logger = logging.getLogger(__name__)


class S3Bucket(APIView):
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

    def delete(self, request):
        data = request.data

        # Check bucketname available
        if 'bucket_name' not in data or data['bucket_name'] == '':
            logger.error({'message': S3_MESSAGE['EMPTY_BUCKET_NAME']})
            return Response({'message': S3_MESSAGE['EMPTY_BUCKET_NAME']}, status=status.HTTP_400_BAD_REQUEST)
        else:
            bucket_name = data['bucket_name']

        s3_client = s3Utility.connect_s3()
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(bucket_name)
        try:
            for key in bucket.objects.all():
                key.delete()
            bucket.delete()
            return Response({'message': S3_MESSAGE['DELETE_BUCKET_SUCCESS']}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error({'message': str(e)})
            logger.error({'message': S3_MESSAGE['DELETE_BUCKET_FAILED']})
            return Response({'message': S3_MESSAGE['DELETE_BUCKET_FAILED']}, status=status.HTTP_400_BAD_REQUEST)

class GetS3Object(APIView):
    permission_classes = (IsAuthenticated,)

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
    permission_classes = (IsAuthenticated,)

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
            'Action': ['s3:List*', 's3:DeleteBucket'],
            'Resource': f'arn:aws:s3:::{bucket_name}'
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
