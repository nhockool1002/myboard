from rest_framework import serializers
from myBoard.s3.models.s3_file_management import S3FileManagement

class S3FileManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = S3FileManagement
        fields = [
            'id',
            'file_name',
            'file_key',
            'bucket_name',
            'created_at',
            'updated_at',
            'created_by',
            'updated_by',
        ]
