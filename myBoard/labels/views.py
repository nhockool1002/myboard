from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework import status
from myBoard.labels.models import ExLabels
from myBoard.labels.serializers import ExLabelsSerializer
from myBoard.labels.messages import EX_LABELS
from django.shortcuts import get_object_or_404

from myBoard.s3.utils import *


import logging
import uuid
import time

logger = logging.getLogger(__name__)


class ExLabelsAPI(APIView):
    permission_classes = (IsAdminUser,)

    def get(self, request):
        data = request.GET
        get_all = False

        if 'label_id' not in data or data['label_id'] == '':
            get_all = True

        if get_all:
            labels = ExLabels.objects.all()
            labels_data = ExLabelsSerializer(labels, many=True)
        else:
            try:
                labels = ExLabels.objects.filter(id=data['label_id']).get()
                labels_data = ExLabelsSerializer(labels)
            except ExLabels.DoesNotExist as e:
                logger.error({'message': str(e)})
                logger.error({'message': EX_LABELS['MYBOARD_LABEL_DOESNT_EXISTS']})
                return Response({'message': EX_LABELS['MYBOARD_LABEL_DOESNT_EXISTS']}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                logger.error({'message': str(e)})
                logger.error({'message': EX_LABELS['MYBOARD_LABEL_GET_FAILED']})
                return Response({'message': EX_LABELS['MYBOARD_LABEL_GET_FAILED']}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"data": labels_data.data if get_all else [labels_data.data]}, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data

        if 'label_name' not in data or data['label_name'] == '':
            logger.error({'message': EX_LABELS['MYBOARD_LABEL_NAME_NOT_FOUND']})
            return Response({'message': EX_LABELS['MYBOARD_LABEL_NAME_NOT_FOUND']}, status=status.HTTP_400_BAD_REQUEST)
        else:
            label_name = data['label_name']

        if 'label_slug' not in data or data['label_slug'] == '':
            logger.error({'message': EX_LABELS['MYBOARD_LABEL_SLUG_NOT_FOUND']})
            return Response({'message': EX_LABELS['MYBOARD_LABEL_SLUG_NOT_FOUND']}, status=status.HTTP_400_BAD_REQUEST)
        else:
            label_slug = data['label_slug']

        if 'label_type' not in data or data['label_type'] == '':
            logger.error({'message': EX_LABELS['MYBOARD_LABEL_TYPE_NOT_FOUND']})
            return Response({'message': EX_LABELS['MYBOARD_LABEL_TYPE_NOT_FOUND']}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if isinstance(data['label_type'], int) and data['label_type'] >= 0:
                label_type = data['label_type']
            else:
                logger.error({'message': EX_LABELS['MYBOARD_LABEL_TYPE_REQUIRE_INT']})
                return Response({'message': EX_LABELS['MYBOARD_LABEL_TYPE_REQUIRE_INT']}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            data = {
                "label_name": label_name,
                "label_slug": label_slug,
                "label_type": label_type,
                "created_by": request.user.username,
                "updated_by": request.user.username
            }
            ExLabels.objects.create(**data)
            return Response({'message': EX_LABELS['MYBOARD_LABEL_CREATE_SUCCESS']}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error({"message": str(e)})
            logger.error({'message': EX_LABELS['MYBOARD_LABEL_CREATE_FAILED']})
            return Response({'message': EX_LABELS['MYBOARD_LABEL_CREATE_FAILED']}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id=None):
        data = request.data

        try:
            if id is not None and isinstance(id, int):
                item = ExLabels.objects.get(id=id)
                serializer = ExLabelsSerializer(item, data=data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response({"status": "success", "data": serializer.data})
                else:
                    return Response({"status": "error", "data": serializer.errors})
            else:
                logger.error({'message': EX_LABELS['MYBOARD_LABEL_ID_NOT_FOUND']})
                return Response({'message': EX_LABELS['MYBOARD_LABEL_ID_NOT_FOUND']}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error({"message": str(e)})
            logger.error({'message': EX_LABELS['MYBOARD_LABEL_UPDATE_FAILED']})
            return Response({'message': EX_LABELS['MYBOARD_LABEL_UPDATE_FAILED']}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id=None):
        try:
            if id is not None and isinstance(id, int):
                item = get_object_or_404(ExLabels, id=id)
                item.delete()
                return Response({"status": "success", "data": "Item Deleted"}, status=status.HTTP_200_OK)
            else:
                logger.error({'message': EX_LABELS['MYBOARD_LABEL_ID_NOT_FOUND']})
                return Response({'message': EX_LABELS['MYBOARD_LABEL_ID_NOT_FOUND']}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error({"message": str(e)})
            logger.error({'message': EX_LABELS['MYBOARD_LABEL_DELETE_FAILED']})
            return Response({'message': EX_LABELS['MYBOARD_LABEL_DELETE_FAILED']}, status=status.HTTP_400_BAD_REQUEST)
