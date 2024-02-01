from django.db import models


class MyBoardNotes(models.Model):
    id = models.AutoField(primary_key=True)
    note_key = models.CharField(max_length=255, blank=True, null=True, unique=True)
    note_content = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=255, blank=True, null=True)
    updated_by = models.CharField(max_length=255, blank=True, null=True)
    

    class Meta:
        db_table = 'myboard_notes'
