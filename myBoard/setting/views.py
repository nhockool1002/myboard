from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status
from myBoard.setting.models import Settings
from myBoard.setting.messages import SETTING
from myBoard.setting.serializers import SettingsSerializer

from myBoard.s3.utils import *


import logging

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
