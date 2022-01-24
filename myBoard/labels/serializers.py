from rest_framework import serializers
from myBoard.labels.models import ExLabels

class ExLabelsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExLabels
        fields = [
            'id',
            'label_name',
            'label_slug',
            'label_type',
            'created_at',
            'updated_at',
            'created_by',
            'updated_by',
        ]
