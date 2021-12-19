from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from myBoard.setting.models import Settings
from myBoard.setting.messages import SETTING
from myBoard.setting.serializers import SettingsSerializer
from rest_framework.parsers import FileUploadParser, MultiPartParser
from myBoard.s3.messages import S3_MESSAGE, S3_FOLDER_MESSAGE
from myBoard.settings import S3_TEMP_FOLDER, THUMBNAILD_ALLOWED_TYPE
from django.core.files.storage import FileSystemStorage

from myBoard.s3.utils import *


import logging
import uuid

logger = logging.getLogger(__name__)


class SettingsAPI(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)

    def get(self, request):
        try:
          settings = Settings.objects.all()
          settings_data = SettingsSerializer(settings, many=True)
          return Response({'data': settings_data.data}, status=status.HTTP_200_OK)
        except Settings.DoesNotExist as e:
          logger.error({"message": str(e)})
          logger.error({'message': SETTING['SETTING_DOES_EXIT']})
          return Response({'message': SETTING['SETTING_DOES_EXIT']}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
          logger.error({"message": str(e)})
          logger.error({'message': SETTING['SETTING_GET_FAILED']})
          return Response({'message': SETTING['SETTING_GET_FAILED']}, status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request):
      data = request.data

      # Check setting key available
      if 'setting_key' not in data or data['setting_key'] == '':
          logger.error({'message': SETTING['SETTING_KEY_NOT_FOUND']})
          return Response({'message': SETTING['SETTING_KEY_NOT_FOUND']}, status=status.HTTP_400_BAD_REQUEST)
      else:
          setting_key = data['setting_key']
      
      # Check setting value available
      if 'setting_value' not in data:
          logger.error({'message': SETTING['SETTING_VALUE_NOT_FOUND']})
          return Response({'message': SETTING['SETTING_VALUE_NOT_FOUND']}, status=status.HTTP_400_BAD_REQUEST)
      else:
          setting_value = data['setting_value']
      
      try:
        setting = Settings.objects.filter(setting_key=setting_key)
        # Update setting
        if setting.count() > 0:
          Settings.objects.filter(setting_key=setting_key).update(setting_value=setting_value)
        # Add new Settings
        else:
          data = {
            "setting_key": setting_key,
            "setting_value": setting_value,
            "created_by": request.user.username,
            "updated_by": request.user.username
          }
          Settings.objects.create(**data)
        return Response({'message': SETTING['SETTING_UPDATE_SUCCESS']}, status=status.HTTP_200_OK)
      except Exception as e:
        logger.error({"message": str(e)})
        logger.error({'message': SETTING['SETTING_UPDATE_FAILED']})
        return Response({'message': SETTING['SETTING_UPDATE_FAILED']}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
      data = request.data

      # Check setting key available
      if 'setting_key' not in data or data['setting_key'] == '':
          logger.error({'message': SETTING['SETTING_KEY_NOT_FOUND']})
          return Response({'message': SETTING['SETTING_KEY_NOT_FOUND']}, status=status.HTTP_400_BAD_REQUEST)
      else:
          setting_key = data['setting_key']
      
      try:
        Settings.objects.filter(setting_key=setting_key).delete()
        return Response({'message': SETTING['SETTING_DELETE_SUCCESS']}, status=status.HTTP_200_OK)
      except Exception as e:
        logger.error({"message": str(e)})
        logger.error({'message': SETTING['SETTING_DELETE_FAILED']})
        return Response({'message': SETTING['SETTING_DELETE_FAILED']}, status=status.HTTP_400_BAD_REQUEST)

class UpdadteThumbSetting(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser)
    parser_class = (FileUploadParser,)

    def post(self, request):
        data = request.data
        uuid_key = uuid.uuid4()
        bucket_name = os.environ["MYBOARD_SETTING_BUCKET"]

        if 'file' not in request.FILES:
            logger.error({'message': S3_FOLDER_MESSAGE['S3_FILE_UPLOAD_NOT_FOUND']})
            return Response({'message': S3_FOLDER_MESSAGE['S3_FILE_UPLOAD_NOT_FOUND']}, status=status.HTTP_400_BAD_REQUEST)
        else:
            img_file = request.FILES['file']


        if 'type' not in data:
            logger.error({'message': S3_FOLDER_MESSAGE['TYPE_NOT_FOUND']})
            return Response({'message': S3_FOLDER_MESSAGE['TYPE_NOT_FOUND']}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if data['type'] not in ['thumb', 'fav']:
              logger.error({'message': S3_FOLDER_MESSAGE['TYPE_NOT_FOUND']})
              return Response({'message': S3_FOLDER_MESSAGE['TYPE_NOT_FOUND']}, status=status.HTTP_400_BAD_REQUEST)
            else:
              typeD = data['type']

        if data['type'] == 'thumb':
          setting_key = 'thumb_image'
        else:
          setting_key = 'fav_image'
        file_name, file_ext = os.path.splitext(img_file.name)
        if file_ext not in THUMBNAILD_ALLOWED_TYPE:
            logger.error({'message': S3_FOLDER_MESSAGE['S3_FILE_UPLOAD_UNVALID_EXT']})
            return Response({'message': S3_FOLDER_MESSAGE['S3_FILE_UPLOAD_UNVALID_EXT']}, status=status.HTTP_400_BAD_REQUEST)
            

        s3_client = s3Utility.connect_s3()
        fs = FileSystemStorage()
        filename = fs.save(f'{S3_TEMP_FOLDER}{uuid_key}-{img_file.name}', img_file)
        uploaded_file_path = fs.path(filename)

        try:
            key = f'thumb/{uuid_key}-{img_file.name}'
            s3_client.upload_file(uploaded_file_path, bucket_name, key, ExtraArgs={'ACL': 'public-read'})
            url = s3Utility.get_object_url(bucket_name, key)
            
            setting = Settings.objects.filter(setting_key=setting_key)
            # Update setting
            if setting.count() > 0:
              Settings.objects.filter(setting_key=setting_key).update(setting_value=url)
            # Add new Settings
            else:
              uploaded_data = {
                "setting_key": setting_key,
                "setting_value": url
              }
              Settings.objects.create(**uploaded_data)
        except Exception as e:
            logger.error({'message': str(e)})
            logger.error({'message': S3_FOLDER_MESSAGE['S3_FILE_UPLOAD_FAILED']})
            return Response({'message': S3_FOLDER_MESSAGE['S3_FILE_UPLOAD_FAILED']}, status=status.HTTP_400_BAD_REQUEST)

        # Remove temp file
        fs.delete(uploaded_file_path)
        return Response({'message': S3_FOLDER_MESSAGE['S3_FILE_UPLOAD_SUCCESS']}, status=status.HTTP_200_OK)