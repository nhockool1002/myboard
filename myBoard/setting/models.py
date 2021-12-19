from django.db import models


class Settings(models.Model):
    id = models.AutoField(primary_key=True)
    setting_key = models.CharField(max_length=255, blank=True, null=True, unique=True)
    setting_value = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=255, blank=True, null=True)
    updated_by = models.CharField(max_length=255, blank=True, null=True)
    

    class Meta:
        db_table = 'settings'
