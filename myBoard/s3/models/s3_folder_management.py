from django.db import models
from myBoard.s3.models.s3_bucket_management import S3BucketManagement

class S3FolderManagement(models.Model):
    id = models.AutoField(primary_key=True)
    folder_name = models.CharField(max_length=255, blank=True, null=True)
    folder_key = models.CharField(max_length=255, blank=True, null=True, unique=True)
    bucket_name = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=255, blank=True, null=True)
    updated_by = models.CharField(max_length=255, blank=True, null=True)
    bucket = models.ForeignKey(
        S3BucketManagement, on_delete=models.CASCADE, to_field="id", null=True, blank=True)

    class Meta:
        db_table = 's3_folder_management'
