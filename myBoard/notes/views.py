from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework import status
from myBoard.notes.models import MyBoardNotes
from myBoard.notes.serializers import MyBoardNotesSerializer
from myBoard.notes.messages import NOTES

from myBoard.s3.utils import *


import logging
import uuid
import time

logger = logging.getLogger(__name__)


class MyBoardNotesAPI(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser,)

    def get(self, request):
        data = request.GET
        get_all = False

        if 'note_id' not in data or data['note_id'] == '':
            get_all = True

        if get_all:
            notes = MyBoardNotes.objects.all()
            notes_data = MyBoardNotesSerializer(notes, many=True)
        else:
            try:
                notes = MyBoardNotes.objects.filter(id=data['note_id']).get()
                notes_data = MyBoardNotesSerializer(notes)
            except MyBoardNotes.DoesNotExist as e:
                logger.error({'message': str(e)})
                logger.error({'message': NOTES['MYBOARD_NOTES_DOESNT_EXISTS']})
                return Response({'message': NOTES['MYBOARD_NOTES_DOESNT_EXISTS']}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                logger.error({'message': str(e)})
                logger.error({'message': NOTES['MYBOARD_NOTES_GET_FAILED']})
                return Response({'message': NOTES['MYBOARD_NOTES_GET_FAILED']}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"data": notes_data.data if get_all else [notes_data.data]}, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data

        if 'note_key' not in data or data['note_key'] == '':
            logger.error({'message': NOTES['MYBOARD_NOTES_KEY_NOT_FOUND']})
            return Response({'message': NOTES['MYBOARD_NOTES_KEY_NOT_FOUND']}, status=status.HTTP_400_BAD_REQUEST)
        else:
            note_key = data['note_key']

        if 'note_content' not in data or data['note_content'] == '':
            logger.error({'message': NOTES['MYBOARD_NOTES_CONTENT_NOT_FOUND']})
            return Response({'message': NOTES['MYBOARD_NOTES_CONTENT_NOT_FOUND']}, status=status.HTTP_400_BAD_REQUEST)
        else:
            note_content = data['note_content']
        
        try:
            note = MyBoardNotes.objects.filter(note_key=note_key)
            # Update setting
            if note.count() > 0:
                logger.error({'message': NOTES['MYBOARD_NOTES_EXISTED']})
                return Response({'message': NOTES['MYBOARD_NOTES_EXISTED']}, status=status.HTTP_400_BAD_REQUEST)
            # Add new Settings
            else:
                data = {
                    "note_key": note_key,
                    "note_content": note_content,
                    "created_by": request.user.username,
                    "updated_by": request.user.username
                }
                MyBoardNotes.objects.create(**data)
                return Response({'message': NOTES['MYBOARD_NOTE_CREATE_SUCCESS']}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error({"message": str(e)})
            logger.error({'message': NOTES['MYBOARD_NOTE_CREATE_FAILED']})
            return Response({'message': NOTES['MYBOARD_NOTE_CREATE_FAILED']}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        data = request.GET

        # Check setting key available
        if 'note_key' not in data or data['note_key'] == '':
                logger.error({'message': NOTES['MYBOARD_NOTES_KEY_NOT_FOUND']})
                return Response({'message': NOTES['MYBOARD_NOTES_KEY_NOT_FOUND']}, status=status.HTTP_400_BAD_REQUEST)
        else:
            note_key = data['note_key']
      
        try:
            MyBoardNotes.objects.filter(note_key=note_key).delete()
            return Response({'message': NOTES['MYBOARD_NOTE_DELETE_SUCCESS']}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error({"message": str(e)})
            logger.error({'message': NOTES['MYBOARD_NOTE_DELETE_SUCCESS']})
            return Response({'message': NOTES['MYBOARD_NOTE_DELETE_SUCCESS']}, status=status.HTTP_400_BAD_REQUEST)

class UpdateNoteAPI(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser,)

    def post(self, request):
        data = request.data

        if 'note_key' not in data or data['note_key'] == '':
            logger.error({'message': NOTES['MYBOARD_NOTES_KEY_NOT_FOUND']})
            return Response({'message': NOTES['MYBOARD_NOTES_KEY_NOT_FOUND']}, status=status.HTTP_400_BAD_REQUEST)
        else:
            note_key = data['note_key']

        if 'note_content' not in data or data['note_content'] == '':
            logger.error({'message': NOTES['MYBOARD_NOTES_CONTENT_NOT_FOUND']})
            return Response({'message': NOTES['MYBOARD_NOTES_CONTENT_NOT_FOUND']}, status=status.HTTP_400_BAD_REQUEST)
        else:
            note_content = data['note_content']
        
        try:
            note = MyBoardNotes.objects.filter(note_key=note_key)
            # Update setting
            if note.count() > 0:
                MyBoardNotes.objects.filter(note_key=note_key).update(note_content=note_content)
                return Response({'message': NOTES['MYBOARD_NOTE_UPDATE_SUCCESS']}, status=status.HTTP_200_OK)
            else:
                logger.error({'message': NOTES['MYBOARD_NOTES_DOESNT_EXISTS']})
                return Response({'message': NOTES['MYBOARD_NOTES_DOESNT_EXISTS']}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error({"message": str(e)})
            logger.error({'message': NOTES['MYBOARD_NOTE_UPDATE_FAILED']})
            return Response({'message': NOTES['MYBOARD_NOTE_UPDATE_FAILED']}, status=status.HTTP_400_BAD_REQUEST)