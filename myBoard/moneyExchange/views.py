from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework import status
from myBoard.setting.models import Settings
from myBoard.setting.messages import SETTING
from myBoard.setting.serializers import SettingsSerializer
from myBoard.moneyExchange.messages import MONEY_EXCHANGE
from django.core.files.storage import FileSystemStorage

from myBoard.s3.utils import *


import logging
import requests
import datetime
import uuid

logger = logging.getLogger(__name__)


class MoneyExchangeAPI(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser,)

    def get(self, request):
        data = request.GET
        base = ''
        amount = ''
        domain = ''
        key = ''
        des = ''
        rates = 0
        result = 0
        
        if 'base' not in data or data['base'] == '':
            logger.error({'message': MONEY_EXCHANGE['MONEY_EXCHANGE_BASE_NOT_FOUND']})
            return Response({'message': MONEY_EXCHANGE['MONEY_EXCHANGE_BASE_NOT_FOUND']}, status=status.HTTP_400_BAD_REQUEST)
        else:
            base = data['base']

        if 'amount' not in data or data['amount'] == '' :
            logger.error({'message': MONEY_EXCHANGE['MONEY_EXCHANGE_AMOUNT_NOT_FOUND']})
            return Response({'message': MONEY_EXCHANGE['MONEY_EXCHANGE_AMOUNT_NOT_FOUND']}, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                amount = float(data['amount'])
                if amount < 0:
                    logger.error({'message': MONEY_EXCHANGE['MONEY_EXCHANGE_AMOUNT_NEED_POSITIVE_NUM']})
                    return Response({'message': MONEY_EXCHANGE['MONEY_EXCHANGE_AMOUNT_NEED_POSITIVE_NUM']}, status=status.HTTP_400_BAD_REQUEST)

            except Exception as e:
                logger.error({'message': str(e)})
                logger.error({'message': MONEY_EXCHANGE['MONEY_EXCHANGE_AMOUNT_REQUIRED_NUM']})
                return Response({'message': MONEY_EXCHANGE['MONEY_EXCHANGE_AMOUNT_REQUIRED_NUM']}, status=status.HTTP_400_BAD_REQUEST)

        if 'des' not in data or data['des'] == '':
            logger.error({'message': MONEY_EXCHANGE['MONEY_EXCHANGE_DES_NOT_FOUND']})
            return Response({'message': MONEY_EXCHANGE['MONEY_EXCHANGE_DES_NOT_FOUND']}, status=status.HTTP_400_BAD_REQUEST)
        else:
            des = data['des']

        if base == des:
            logger.error({'message': MONEY_EXCHANGE['MONEY_EXCHANGE_DES_AND_BASE_AS_SAME']})
            return Response({'message': MONEY_EXCHANGE['MONEY_EXCHANGE_DES_AND_BASE_AS_SAME']}, status=status.HTTP_400_BAD_REQUEST)
        
        settings = Settings.objects.all()
        settings_data = SettingsSerializer(settings, many=True)

        for item in settings_data.data:
            if item['setting_key'] == 'money_exchange_domain':
                domain = item['setting_value']
            if item['setting_key'] == 'money_exchange_key':
                key = item['setting_value']
        
        if domain == '':
            logger.error({'message': MONEY_EXCHANGE['MONEY_EXCHANGE_DOMAIN_SETTING_NOT_FOUND']})
            return Response({'message': MONEY_EXCHANGE['MONEY_EXCHANGE_DOMAIN_SETTING_NOT_FOUND']}, status=status.HTTP_400_BAD_REQUEST)

        if key == '':
            logger.error({'message': MONEY_EXCHANGE['MONEY_EXCHANGE_KEY_SETTING_NOT_FOUND']})
            return Response({'message': MONEY_EXCHANGE['MONEY_EXCHANGE_KEY_SETTING_NOT_FOUND']}, status=status.HTTP_400_BAD_REQUEST)

        list_data = requests.get('%s/api/v2/latest?apikey=%s&base_currency=%s' % (domain, key, base))
        list_currency = list_data.json()['data']

        if des not in list_currency:
            logger.error({'message': MONEY_EXCHANGE['MONEY_EXCHANGE_DES_NOT_IN_LIST']})
            return Response({'message': MONEY_EXCHANGE['MONEY_EXCHANGE_DES_NOT_IN_LIST']}, status=status.HTTP_400_BAD_REQUEST)
        else:
            rates = list_currency[des]
        result = amount*rates
        return Response({"result": result})

class HistoricalMoneyAPI(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser,)

    def get(self, request):
        data = request.GET
        base = ''
        des = ''
        start_date = ''
        end_date = ''
        date_format = '%Y-%m-%d'

        if 'base' not in data or data['base'] == '':
            logger.error({'message': MONEY_EXCHANGE['MONEY_EXCHANGE_BASE_NOT_FOUND']})
            return Response({'message': MONEY_EXCHANGE['MONEY_EXCHANGE_BASE_NOT_FOUND']}, status=status.HTTP_400_BAD_REQUEST)
        else:
            base = data['base']
        
        if 'des' not in data or data['des'] == '':
            logger.error({'message': MONEY_EXCHANGE['MONEY_EXCHANGE_DES_NOT_FOUND']})
            return Response({'message': MONEY_EXCHANGE['MONEY_EXCHANGE_DES_NOT_FOUND']}, status=status.HTTP_400_BAD_REQUEST)
        else:
            des = data['des']
        
        if 'start_date' not in data or data['start_date'] == '':
            logger.error({'message': MONEY_EXCHANGE['MONEY_EXCHANGE_STARTDATE_NOT_FOUND']})
            return Response({'message': MONEY_EXCHANGE['MONEY_EXCHANGE_STARTDATE_NOT_FOUND']}, status=status.HTTP_400_BAD_REQUEST)
        else:
            start_date = data['start_date']
        
        if 'end_date' not in data or data['end_date'] == '':
            logger.error({'message': MONEY_EXCHANGE['MONEY_EXCHANGE_ENDDATE_NOT_FOUND']})
            return Response({'message': MONEY_EXCHANGE['MONEY_EXCHANGE_ENDDATE_NOT_FOUND']}, status=status.HTTP_400_BAD_REQUEST)
        else:
            end_date = data['end_date']

        try:
            datetime.datetime.strptime(start_date, date_format)
        except Exception as e:
            logger.error({'message': str(e)})
            logger.error({'message': MONEY_EXCHANGE['MONEY_EXCHANGE_STARTDATE_INVALID']})
            return Response({'message': MONEY_EXCHANGE['MONEY_EXCHANGE_STARTDATE_INVALID']}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            datetime.datetime.strptime(end_date, date_format)
        except Exception as e:
            logger.error({'message': str(e)})
            logger.error({'message': MONEY_EXCHANGE['MONEY_EXCHANGE_ENDDATE_INVALID']})
            return Response({'message': MONEY_EXCHANGE['MONEY_EXCHANGE_ENDDATE_INVALID']}, status=status.HTTP_400_BAD_REQUEST)
        
        if base == des:
            logger.error({'message': MONEY_EXCHANGE['MONEY_EXCHANGE_DES_AND_BASE_AS_SAME']})
            return Response({'message': MONEY_EXCHANGE['MONEY_EXCHANGE_DES_AND_BASE_AS_SAME']}, status=status.HTTP_400_BAD_REQUEST)

        settings = Settings.objects.all()
        settings_data = SettingsSerializer(settings, many=True)

        for item in settings_data.data:
            if item['setting_key'] == 'money_exchange_domain':
                domain = item['setting_value']
            if item['setting_key'] == 'money_exchange_key':
                key = item['setting_value']
        
        if domain == '':
            logger.error({'message': MONEY_EXCHANGE['MONEY_EXCHANGE_DOMAIN_SETTING_NOT_FOUND']})
            return Response({'message': MONEY_EXCHANGE['MONEY_EXCHANGE_DOMAIN_SETTING_NOT_FOUND']}, status=status.HTTP_400_BAD_REQUEST)

        if key == '':
            logger.error({'message': MONEY_EXCHANGE['MONEY_EXCHANGE_KEY_SETTING_NOT_FOUND']})
            return Response({'message': MONEY_EXCHANGE['MONEY_EXCHANGE_KEY_SETTING_NOT_FOUND']}, status=status.HTTP_400_BAD_REQUEST)

        list_data = requests.get('%s/v3/historical?apikey=%s&base_currency=%s&date_from=%s&date_to=%s' % (domain, key, base, start_date, end_date))
        list_historical = list_data.json()['data']

        list_key = []
        list_money_historical = []
        for key in list_historical.keys():
            list_key.append(key)
        
        for data_money in list_historical:
            list_money_historical.append(list_data.json()['data'][data_money][des])

        return Response({"list_key": list_key, "list_historical": list_money_historical})