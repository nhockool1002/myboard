from django.db import models


class License(models.Model):
    id = models.AutoField(primary_key=True)
    license_name = models.CharField(blank=True, max_length=255, null=True, unique=True)
    license_client_id = models.CharField(blank=True, max_length=255, null=True, unique=True)
    license_private_key = models.TextField(blank=True, null=True)
    license_created_at = models.DateTimeField(auto_now_add=True)
    license_expired_at = models.DateTimeField(auto_now_add=True)
    license_status = models.BooleanField(blank=True, null=True, default=0)
    created_by = models.CharField(max_length=255, blank=True, null=True)
    updated_by = models.CharField(max_length=255, blank=True, null=True)


    class Meta:
        db_table = 'license'
