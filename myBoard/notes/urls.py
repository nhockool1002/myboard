from django.urls import path
from myBoard.notes.views import MyBoardNotesAPI, UpdateNoteAPI
urlpatterns = [
    path('notes/', MyBoardNotesAPI.as_view(), name='notes'),
    path('update-notes/', UpdateNoteAPI.as_view(), name='update_notes'),
]
