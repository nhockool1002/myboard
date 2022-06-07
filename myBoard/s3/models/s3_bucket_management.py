from django.db import models


class S3BucketManagement(models.Model):
    id = models.AutoField(primary_key=True)
    bucket_name = models.CharField(max_length=255, blank=True, null=True)
    bucket_region = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=255, blank=True, null=True)
    updated_by = models.CharField(max_length=255, blank=True, null=True)
    status = models.BooleanField(blank=True, null=False)

    class Meta:
        db_table = 's3_bucket_management'
