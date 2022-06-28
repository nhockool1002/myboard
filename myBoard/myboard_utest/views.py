from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework import status
from myBoard.setting.models import Settings
from myBoard.setting.messages import SETTING
from myBoard.setting.serializers import SettingsSerializer
from myBoard.myboard_utest.messages import UTEST_API_MESSAGE


import logging
import requests

logger = logging.getLogger(__name__)

settings = Settings.objects.all()
settings_data = SettingsSerializer(settings, many=True)

class MyBoardUtestPaymentsAPI(APIView):
	permission_classes = (IsAuthenticated, IsAdminUser,)

	def get(self, request):
		data = request.GET
		get_all = False

		if 'utest_payment_id' not in data or data['utest_payment_id'] == '':
			get_all = True

		for item in settings_data.data:
			if item['setting_key'] == 'utest_api_platform_domain':
					domain = item['setting_value']
			if item['setting_key'] == 'utest_api_token':
					key = item['setting_value']
		if domain == '':
			logger.error({'message': UTEST_API_MESSAGE['UTEST_DOMAIN_SETTING_NOTFOUND']})
			return Response({'message': UTEST_API_MESSAGE['UTEST_DOMAIN_SETTING_NOTFOUND']}, status=status.HTTP_400_BAD_REQUEST)

		if key == '':
			logger.error({'message': UTEST_API_MESSAGE['UTEST_TOKEN_SETTING_NOTFOUND']})
			return Response({'message': UTEST_API_MESSAGE['UTEST_TOKEN_SETTING_NOTFOUND']}, status=status.HTTP_400_BAD_REQUEST)

		headers = {"Authorization": "Bearer %s" % (key)}
		
		if get_all:
			url = '%sprofile/payments' % (domain)
		else:
			url = '%sprofile/payments/%s' % (domain, data['utest_payment_id'])

		list_data = requests.get(url, headers=headers).json()
		if "message" in list_data:
			return Response({'data': list_data["message"]}, status=status.HTTP_400_BAD_REQUEST)
		else :
			if 'totalPayout' in list_data["data"] and 'pendingPayout' in list_data['data']:
				return Response(
					{
						'data': list_data["data"]["paymentHistory"] if get_all else list_data["data"],
						'totalPayout': list_data['data']['totalPayout'],
						'pendingPayout': list_data['data']['pendingPayout']
					}, 
					status=status.HTTP_200_OK
				)
			else:
				return Response(
					{
						'data': list_data["data"]["paymentHistory"] if get_all else list_data["data"],
					}, 
					status=status.HTTP_200_OK
				)

class MyBoardUtestProfileAPI(APIView):
	permission_classes = (IsAuthenticated, IsAdminUser,)

	def get(self, request):
		data = request.GET

		for item in settings_data.data:
			if item['setting_key'] == 'utest_api_domain':
					domain = item['setting_value']
			if item['setting_key'] == 'utest_api_token':
					key = item['setting_value']

		if domain == '':
			logger.error({'message': UTEST_API_MESSAGE['UTEST_DOMAIN_SETTING_NOTFOUND']})
			return Response({'message': UTEST_API_MESSAGE['UTEST_DOMAIN_SETTING_NOTFOUND']}, status=status.HTTP_400_BAD_REQUEST)

		if key == '':
			logger.error({'message': UTEST_API_MESSAGE['UTEST_TOKEN_SETTING_NOTFOUND']})
			return Response({'message': UTEST_API_MESSAGE['UTEST_TOKEN_SETTING_NOTFOUND']}, status=status.HTTP_400_BAD_REQUEST)

		headers = {"Authorization": "Bearer %s" % (key)}

		list_data = requests.get('%susers/me' % (domain), headers=headers).json()

		if "errors" in list_data:
			return Response({'data': list_data["errors"]}, status=status.HTTP_400_BAD_REQUEST)
		else:
			return Response({'data': list_data}, status=status.HTTP_200_OK)

class MyBoardUtestBugsInTestCycleAPI(APIView):
	permission_classes = (IsAuthenticated, IsAdminUser,)

	def get(self, request):
		data = request.GET

		for item in settings_data.data:
			if item['setting_key'] == 'utest_api_platform_domain':
				domain = item['setting_value']
			if item['setting_key'] == 'utest_api_token':
				key = item['setting_value']
			if item['setting_key'] == 'utest_tester_id':
				testerId = item['setting_value']

		testCyclesId = ''

		if domain == '':
			logger.error({'message': UTEST_API_MESSAGE['UTEST_DOMAIN_SETTING_NOTFOUND']})
			return Response({'message': UTEST_API_MESSAGE['UTEST_DOMAIN_SETTING_NOTFOUND']}, status=status.HTTP_400_BAD_REQUEST)

		if key == '':
			logger.error({'message': UTEST_API_MESSAGE['UTEST_TOKEN_SETTING_NOTFOUND']})
			return Response({'message': UTEST_API_MESSAGE['UTEST_TOKEN_SETTING_NOTFOUND']}, status=status.HTTP_400_BAD_REQUEST)

		if testerId == '':
			logger.error({'message': UTEST_API_MESSAGE['UTEST_TESTER_ID_NOTFOUND']})
			return Response({'message': UTEST_API_MESSAGE['UTEST_TESTER_ID_NOTFOUND']}, status=status.HTTP_400_BAD_REQUEST)
		
		if 'testCycleId' not in data or data['testCycleId'] == '':
			logger.error({'message': UTEST_API_MESSAGE['UTEST_TEST_CYCLE_ID_NOTFOUND']})
			return Response({'message': UTEST_API_MESSAGE['UTEST_TEST_CYCLE_ID_NOTFOUND']}, status=status.HTTP_400_BAD_REQUEST)
		else:
			testCyclesId = data['testCycleId']
		
		headers = {"Authorization": "Bearer %s" % (key)}

		list_data = requests.get('%sbugs?testCycleId=%s&testerId=%s&resolved=true&iDisplayLength=100000' % (domain, testCyclesId, testerId), headers=headers).json()

		if "message" in list_data:
			return Response({'data': list_data["message"]}, status=status.HTTP_400_BAD_REQUEST)
		else :
			return Response({'data': list_data["data"]}, status=status.HTTP_200_OK)

class MyBoardUtestTestcasesInTestCycleAPI(APIView):
	permission_classes = (IsAuthenticated, IsAdminUser,)

	def get(self, request):
		data = request.GET

		for item in settings_data.data:
			if item['setting_key'] == 'utest_api_platform_domain':
				domain = item['setting_value']
			if item['setting_key'] == 'utest_api_token':
				key = item['setting_value']
			if item['setting_key'] == 'utest_tester_id':
				testerId = item['setting_value']

		testCyclesId = ''

		if domain == '':
			logger.error({'message': UTEST_API_MESSAGE['UTEST_DOMAIN_SETTING_NOTFOUND']})
			return Response({'message': UTEST_API_MESSAGE['UTEST_DOMAIN_SETTING_NOTFOUND']}, status=status.HTTP_400_BAD_REQUEST)

		if key == '':
			logger.error({'message': UTEST_API_MESSAGE['UTEST_TOKEN_SETTING_NOTFOUND']})
			return Response({'message': UTEST_API_MESSAGE['UTEST_TOKEN_SETTING_NOTFOUND']}, status=status.HTTP_400_BAD_REQUEST)
		
		if 'testCycleId' not in data or data['testCycleId'] == '':
			logger.error({'message': UTEST_API_MESSAGE['UTEST_TEST_CYCLE_ID_NOTFOUND']})
			return Response({'message': UTEST_API_MESSAGE['UTEST_TEST_CYCLE_ID_NOTFOUND']}, status=status.HTTP_400_BAD_REQUEST)
		else:
			testCyclesId = data['testCycleId']
		
		headers = {"Authorization": "Bearer %s" % (key)}

		list_data = requests.get('%stestruns/results?testCycleId=%s' % (domain, testCyclesId), headers=headers).json()

		if "message" in list_data:
			return Response({'data': list_data["message"]}, status=status.HTTP_400_BAD_REQUEST)
		else :
			return Response({'data': list_data["data"]}, status=status.HTTP_200_OK)

class MyBoardUtestPreApprovePaymentAPI(APIView):
	permission_classes = (IsAuthenticated, IsAdminUser,)

	def get(self, request):
		for item in settings_data.data:
			if item['setting_key'] == 'utest_api_platform_domain':
				domain = item['setting_value']
			if item['setting_key'] == 'utest_api_token':
				key = item['setting_value']

		if domain == '':
			logger.error({'message': UTEST_API_MESSAGE['UTEST_DOMAIN_SETTING_NOTFOUND']})
			return Response({'message': UTEST_API_MESSAGE['UTEST_DOMAIN_SETTING_NOTFOUND']}, status=status.HTTP_400_BAD_REQUEST)

		if key == '':
			logger.error({'message': UTEST_API_MESSAGE['UTEST_TOKEN_SETTING_NOTFOUND']})
			return Response({'message': UTEST_API_MESSAGE['UTEST_TOKEN_SETTING_NOTFOUND']}, status=status.HTTP_400_BAD_REQUEST)
		
		headers = {"Authorization": "Bearer %s" % (key)}

		list_data = requests.get('%sprofile/payments/preapproved' % (domain), headers=headers).json()

		if "message" in list_data:
			return Response({'data': list_data["message"]}, status=status.HTTP_400_BAD_REQUEST)
		else :
			return Response({'data': list_data["data"]}, status=status.HTTP_200_OK)

class MyBoardUtestActivityAPI(APIView):
	permission_classes = (IsAuthenticated, IsAdminUser,)

	def get(self, request):
		data = request.GET

		if 'page' not in data or data['page'] == '':
			logger.error({'message': UTEST_API_MESSAGE['UTEST_PAGE_ACTIVITY_NOTFOUND']})
			return Response({'message': UTEST_API_MESSAGE['UTEST_PAGE_ACTIVITY_NOTFOUND']}, status=status.HTTP_400_BAD_REQUEST)
		else:
			page = data['page']

		for item in settings_data.data:
			if item['setting_key'] == 'utest_api_domain':
				domain = item['setting_value']
			if item['setting_key'] == 'utest_api_token':
				key = item['setting_value']
		
		if domain == '':
			logger.error({'message': UTEST_API_MESSAGE['UTEST_DOMAIN_SETTING_NOTFOUND']})
			return Response({'message': UTEST_API_MESSAGE['UTEST_DOMAIN_SETTING_NOTFOUND']}, status=status.HTTP_400_BAD_REQUEST)

		if key == '':
			logger.error({'message': UTEST_API_MESSAGE['UTEST_TOKEN_SETTING_NOTFOUND']})
			return Response({'message': UTEST_API_MESSAGE['UTEST_TOKEN_SETTING_NOTFOUND']}, status=status.HTTP_400_BAD_REQUEST)

		headers = {"Authorization": "Bearer %s" % (key)}

		list_data = requests.get('%sactivities?page=%s&per_page=50' % (domain, page), headers=headers).json()

		if "message" in list_data:
			return Response({'data': list_data["message"]}, status=status.HTTP_400_BAD_REQUEST)
		else :
			return Response({'data': list_data}, status=status.HTTP_200_OK)
