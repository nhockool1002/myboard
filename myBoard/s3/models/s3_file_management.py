from django.db import models
from myBoard.s3.models.s3_folder_management import S3FolderManagement
from myBoard.s3.models.s3_bucket_management import S3BucketManagement


class S3FileManagement(models.Model):
    id = models.AutoField(primary_key=True)
    file_name = models.CharField(max_length=255, blank=True, null=True)
    file_key = models.CharField(max_length=255, blank=True, null=True)
    bucket_name = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=255, blank=True, null=True)
    updated_by = models.CharField(max_length=255, blank=True, null=True)
    file_type = models.CharField(max_length=255, blank=True, null=True)
    folder = models.ForeignKey(
        S3FolderManagement, on_delete=models.CASCADE, to_field="id", null=True, blank=True)
    bucket = models.ForeignKey(
        S3BucketManagement, on_delete=models.CASCADE, to_field="id", null=True, blank=True)

    class Meta:
        db_table = 's3_file_management'
