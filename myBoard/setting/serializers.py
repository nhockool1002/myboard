from rest_framework import serializers
from myBoard.setting.models import Settings

class SettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Settings
        fields = [
            'id',
            'setting_key',
            'setting_value',
            'created_at',
            'updated_at',
            'created_by',
            'updated_by',
        ]
