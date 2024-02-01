from rest_framework import serializers
from myBoard.notes.models import MyBoardNotes

class MyBoardNotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyBoardNotes
        fields = [
            'id',
            'note_key',
            'note_content',
            'created_at',
            'updated_at',
            'created_by',
            'updated_by',
        ]
