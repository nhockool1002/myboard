from rest_framework import serializers
from myBoard.license.models import License

class LicenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = License
        fields = [
            'id',
            'license_name',
            'license_client_id',
            'license_private_key',
            'license_created_at',
            'license_expired_at',
            'license_status',
            'created_by',
            'updated_by'
        ]
