from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework import status
from myBoard.categories.models import ExCategories
from myBoard.categories.serializers import ExCategoriesSerializer
from myBoard.categories.messages import EX_CATEGORIES
from django.shortcuts import get_object_or_404

from myBoard.s3.utils import *


import logging
import uuid
import time

logger = logging.getLogger(__name__)


class ExCategoriesAPI(APIView):
    permission_classes = (IsAdminUser,)

    def get(self, request):
        data = request.GET
        get_all = False

        if 'cat_id' not in data or data['cat_id'] == '':
            get_all = True

        if get_all:
            cats = ExCategories.objects.all()
            cats_data = ExCategoriesSerializer(cats, many=True)
        else:
            try:
                cats = ExCategories.objects.filter(id=data['cat_id']).get()
                cats_data = ExCategoriesSerializer(cats)
            except ExCategories.DoesNotExist as e:
                logger.error({'message': str(e)})
                logger.error({'message': EX_CATEGORIES['MYBOARD_CAT_DOESNT_EXISTS']})
                return Response({'message': EX_CATEGORIES['MYBOARD_CAT_DOESNT_EXISTS']}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                logger.error({'message': str(e)})
                logger.error({'message': EX_CATEGORIES['MYBOARD_CAT_GET_FAILED']})
                return Response({'message': EX_CATEGORIES['MYBOARD_CAT_GET_FAILED']}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"data": cats_data.data if get_all else [cats_data.data]}, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data

        if 'cat_name' not in data or data['cat_name'] == '':
            logger.error({'message': EX_CATEGORIES['MYBOARD_CAT_NAME_NOT_FOUND']})
            return Response({'message': EX_CATEGORIES['MYBOARD_CAT_NAME_NOT_FOUND']}, status=status.HTTP_400_BAD_REQUEST)
        else:
            cat_name = data['cat_name']

        if 'cat_slug' not in data or data['cat_slug'] == '':
            logger.error({'message': EX_CATEGORIES['MYBOARD_CAT_SLUG_NOT_FOUND']})
            return Response({'message': EX_CATEGORIES['MYBOARD_CAT_SLUG_NOT_FOUND']}, status=status.HTTP_400_BAD_REQUEST)
        else:
            cat_slug = data['cat_slug']

        if 'order' not in data or data['order'] == '':
            logger.error({'message': EX_CATEGORIES['MYBOARD_CAT_ORDER_NOT_FOUND']})
            return Response({'message': EX_CATEGORIES['MYBOARD_CAT_ORDER_NOT_FOUND']}, status=status.HTTP_400_BAD_REQUEST)
        else:
            order = data['order']
        
        if 'sticky' not in data or data['sticky'] == '':
            logger.error({'message': EX_CATEGORIES['MYBOARD_CAT_STICKY_NOT_FOUND']})
            return Response({'message': EX_CATEGORIES['MYBOARD_CAT_STICKY_NOT_FOUND']}, status=status.HTTP_400_BAD_REQUEST)
        else:
            sticky = data['sticky']
        
        try:
            data = {
                "category_name": cat_name,
                "category_slug": cat_slug,
                "order": order,
                "sticky": sticky,
                "created_by": request.user.username,
                "updated_by": request.user.username
            }
            ExCategories.objects.create(**data)
            return Response({'message': EX_CATEGORIES['MYBOARD_CAT_CREATE_SUCCESS']}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error({"message": str(e)})
            logger.error({'message': EX_CATEGORIES['MYBOARD_CAT_CREATE_FAILED']})
            return Response({'message': EX_CATEGORIES['MYBOARD_CAT_CREATE_FAILED']}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id=None):
        data = request.data

        try:
            if id is not None and isinstance(id, int):
                item = ExCategories.objects.get(id=id)
                serializer = ExCategoriesSerializer(item, data=data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response({"status": "success", "data": serializer.data})
                else:
                    return Response({"status": "error", "data": serializer.errors})
            else:
                logger.error({'message': EX_CATEGORIES['MYBOARD_CAT_ID_NOT_FOUND']})
                return Response({'message': EX_CATEGORIES['MYBOARD_CAT_ID_NOT_FOUND']}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error({"message": str(e)})
            logger.error({'message': EX_CATEGORIES['MYBOARD_CAT_UPDATE_FAILED']})
            return Response({'message': EX_CATEGORIES['MYBOARD_CAT_UPDATE_FAILED']}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id=None):
        try:
            if id is not None and isinstance(id, int):
                item = get_object_or_404(ExCategories, id=id)
                item.delete()
                return Response({"status": "success", "data": "Item Deleted"}, status=status.HTTP_200_OK)
            else:
                logger.error({'message': EX_CATEGORIES['MYBOARD_CAT_ID_NOT_FOUND']})
                return Response({'message': EX_CATEGORIES['MYBOARD_CAT_ID_NOT_FOUND']}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error({"message": str(e)})
            logger.error({'message': EX_CATEGORIES['MYBOARD_CAT_DELETE_FAILED']})
            return Response({'message': EX_CATEGORIES['MYBOARD_CAT_DELETE_FAILED']}, status=status.HTTP_400_BAD_REQUEST)


