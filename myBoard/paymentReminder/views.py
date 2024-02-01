from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework import status
from myBoard.paymentReminder.models import MyBoardPaymentReminder
from myBoard.paymentReminder.serializers import MyBoardPaymentReminderSerializer
from django.shortcuts import get_object_or_404
from myBoard.paymentReminder.messages import PAYMENT_REMINDER
from myBoard.s3.utils import *

logger = logging.getLogger(__name__)

class MyBoardPaymentReminderAPI(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser,)
    
    def get(self, request):
        data = request.GET
        get_all = False

        if 'payment_reminder_id' not in data or data['payment_reminder_id'] == '':
            get_all = True

        if get_all:
            paymentReminders = MyBoardPaymentReminder.objects.all()
            paymentReminders_data = MyBoardPaymentReminderSerializer(paymentReminders, many=True)
        else:
            try:
                paymentReminders = MyBoardPaymentReminder.objects.filter(id=data['payment_reminder_id']).get()
                paymentReminders_data = MyBoardPaymentReminderSerializer(paymentReminders)
            except MyBoardPaymentReminder.DoesNotExist as e:
                logger.error({'message': str(e)})
                logger.error({'message': PAYMENT_REMINDER['MYBOARD_PAYMENT_REMINDER_DOESNT_EXISTS']})
                return Response({'message': PAYMENT_REMINDER['MYBOARD_PAYMENT_REMINDER_DOESNT_EXISTS']}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                logger.error({'message': str(e)})
                logger.error({'message': PAYMENT_REMINDER['MYBOARD_PAYMENT_REMINDER_GET_FAILED']})
                return Response({'message': PAYMENT_REMINDER['MYBOARD_PAYMENT_REMINDER_GET_FAILED']}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"data": paymentReminders_data.data if get_all else [paymentReminders_data.data]}, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data

        if 'payment_name' not in data or data['payment_name'] == '':
            logger.error({'message': PAYMENT_REMINDER['MYBOARD_PAYMENT_NAME_NOT_FOUND']})
            return Response({'message': PAYMENT_REMINDER['MYBOARD_PAYMENT_NAME_NOT_FOUND']}, status=status.HTTP_400_BAD_REQUEST)
        else:
            payment_name = data['payment_name']
        
        if 'payment_content' not in data or data['payment_content'] == '':
            logger.error({'message': PAYMENT_REMINDER['MYBOARD_PAYMENT_CONTENT_NOT_FOUND']})
            return Response({'message': PAYMENT_REMINDER['MYBOARD_PAYMENT_CONTENT_NOT_FOUND']}, status=status.HTTP_400_BAD_REQUEST)
        else:
            payment_content = data['payment_content']

        if 'payment_due_date' not in data or data['payment_due_date'] == '':
            logger.error({'message': PAYMENT_REMINDER['MYBOARD_PAYMENT_DUEDATE_NOT_FOUND']})
            return Response({'message': PAYMENT_REMINDER['MYBOARD_PAYMENT_DUEDATE_NOT_FOUND']}, status=status.HTTP_400_BAD_REQUEST)
        else:
            payment_due_date = data['payment_due_date']
        
        if 'payment_price' not in data or data['payment_price'] == '':
            logger.error({'message': PAYMENT_REMINDER['MYBOARD_PAYMENT_PRICE_NOT_FOUND']})
            return Response({'message': PAYMENT_REMINDER['MYBOARD_PAYMENT_PRICE_NOT_FOUND']}, status=status.HTTP_400_BAD_REQUEST)
        else:
            payment_price = data['payment_price']

        if 'payment_status' not in data or data['payment_status'] == '':
            payment_status = 0
        else: 
            arrayData = [0, 1]
            exists = int(data['payment_status']) in arrayData
            print(exists)
            if exists:
                payment_status = int(data['payment_status'])
            else: 
                logger.error({'message': PAYMENT_REMINDER['MYBOARD_PAYMENT_STATUS_NOT_VALID']})
                return Response({'message': PAYMENT_REMINDER['MYBOARD_PAYMENT_STATUS_NOT_VALID']}, status=status.HTTP_400_BAD_REQUEST)
        try:
            data = {
                "payment_name": payment_name,
                "payment_content": payment_content,
                "payment_due_date": payment_due_date,
                "payment_price": payment_price,
                "payment_status": payment_status,
                "created_by": request.user.username,
                "updated_by": request.user.username
            }
            added = MyBoardPaymentReminder.objects.create(**data)
            added_data = MyBoardPaymentReminderSerializer(added)
            return Response({'message': PAYMENT_REMINDER['MYBOARD_PAYMENT_REMINDER_CREATE_SUCCESS'], 'data': added_data.data}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error({"message": str(e)})
            logger.error({'message': PAYMENT_REMINDER['MYBOARD_PAYMENT_REMINDER_CREATE_FAILED']})
            return Response({'message': PAYMENT_REMINDER['MYBOARD_PAYMENT_REMINDER_CREATE_FAILED']}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id=None):
        data = request.data
        print(data)
        try:
            if id is not None and isinstance(id, int):
                item = MyBoardPaymentReminder.objects.get(id=id)
                serializer = MyBoardPaymentReminderSerializer(item, data=data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response({"status": "success", "data": serializer.data})
                else:
                    return Response({"status": "error", "data": serializer.errors})
            else:
                logger.error({'message': PAYMENT_REMINDER['MYBOARD_PAYMENT_REMINDER_ID_NOT_FOUND']})
                return Response({'message': PAYMENT_REMINDER['MYBOARD_PAYMENT_REMINDER_ID_NOT_FOUND']}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error({"message": str(e)})
            logger.error({'message': PAYMENT_REMINDER['MYBOARD_PAYMENT_REMINDER_UPDATE_FAILED']})
            return Response({'message': PAYMENT_REMINDER['MYBOARD_PAYMENT_REMINDER_UPDATE_FAILED']}, status=status.HTTP_400_BAD_REQUEST) 

    def delete(self, request, id=None):
        try:
            if id is not None and isinstance(id, int):
                item = get_object_or_404(MyBoardPaymentReminder, id=id)
                item.delete()
                return Response({"status": "success", "data": "Item Deleted"}, status=status.HTTP_200_OK)
            else:
                logger.error({'message': PAYMENT_REMINDER['MYBOARD_PAYMENT_REMINDER_ID_NOT_FOUND']})
                return Response({'message': PAYMENT_REMINDER['MYBOARD_PAYMENT_REMINDER_ID_NOT_FOUND']}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error({"message": str(e)})
            logger.error({'message': PAYMENT_REMINDER['MYBOARD_PAYMENT_REMINDER_DELETE_FAILED']})
            return Response({'message': PAYMENT_REMINDER['MYBOARD_PAYMENT_REMINDER_DELETE_FAILED']}, status=status.HTTP_400_BAD_REQUEST) 

