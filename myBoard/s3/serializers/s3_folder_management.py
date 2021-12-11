from rest_framework import serializers
from myBoard.s3.models.s3_folder_management import S3FolderManagement

class S3FolderManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = S3FolderManagement
        fields = [
            'id',
            'folder_name',
            'folder_key',
            'bucket_name',
            'created_at',
            'updated_at',
            'created_by',
            'updated_by',
        ]
