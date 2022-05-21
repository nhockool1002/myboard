from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework import status
from myBoard.license.models import License
from myBoard.license.serializers import LicenseSerializer
from myBoard.license.messages import LICENSE
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

from myBoard.s3.utils import *


import logging
import uuid
import time
import bcrypt
import os
import hashlib
import json

logger = logging.getLogger(__name__)


class LicenseAPI(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        data = request.GET
        # Check params
        if 'license_name' not in data or data['license_name'] == '':
            logger.error({'message': LICENSE['LICENSE_NAME_MISSING']})
            return Response({'message': LICENSE['LICENSE_NAME_MISSING']}, status=status.HTTP_400_BAD_REQUEST)
        else:
            license_name = data['license_name']

        if 'license_client_id' not in data or data['license_client_id'] == '':
            logger.error({'message': LICENSE['LICENSE_CLIENT_MISSING']})
            return Response({'message': LICENSE['LICENSE_CLIENT_MISSING']}, status=status.HTTP_400_BAD_REQUEST)
        else:
            license_client_id = data['license_client_id']

        if 'license_private_key' not in data or data['license_private_key'] == '':
            logger.error({'message': LICENSE['LICENSE_PRIVATE_MISSING']})
            return Response({'message': LICENSE['LICENSE_PRIVATE_MISSING']}, status=status.HTTP_400_BAD_REQUEST)
        else:
            license_private_key = data['license_private_key']

        obj = License.objects.filter(
            license_private_key=license_private_key,
            license_name=license_name,
            license_client_id=license_client_id
        )

        if (obj.count() > 0):
            obj_data = LicenseSerializer(obj, many=True)
        else:
            return Response({'message': LICENSE['LICENSE_NOT_EXISTED']}, status=status.HTTP_400_BAD_REQUEST)

        res = Response({"data": obj_data.data, "status": status.HTTP_200_OK})
        res['Access-Control-Allow-Origin'] = '*'
        return res

    def post(self, request):
        data = request.data

        if 'license_name' not in data or data['license_name'] == '':
            logger.error({'message': LICENSE['LICENSE_NAME_MISSING']})
            return Response({'message': LICENSE['LICENSE_NAME_MISSING']}, status=status.HTTP_400_BAD_REQUEST)
        else:
            license_name = data['license_name']

        if 'license_client_id' not in data or data['license_client_id'] == '':
            logger.error({'message': LICENSE['LICENSE_CLIENT_MISSING']})
            return Response({'message': LICENSE['LICENSE_CLIENT_MISSING']}, status=status.HTTP_400_BAD_REQUEST)
        else:
            license_client_id = data['license_client_id']
        
        pwd = license_name + license_client_id + os.environ["MYBOARD_SECRET_APP_NUMBER"]
        pwd = pwd.encode('UTF-8')

        md5 = hashlib.sha256(pwd).hexdigest()

        try:
            data = {
                "license_name": license_name,
                "license_client_id": license_client_id,
                "license_private_key": hashlib.sha256(pwd).hexdigest(),
                "created_by": request.user.username,
                "updated_by": request.user.username
            }
            License.objects.create(**data)
            return Response({'message': LICENSE['LICENSE_CREATED_SUCCESS']}, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error({"message": str(e)})
            logger.error({'message': LICENSE['LICENSE_CREATED_FAILED']})
            return Response({'message': LICENSE['LICENSE_CREATED_FAILED']}, status=status.HTTP_400_BAD_REQUEST)
