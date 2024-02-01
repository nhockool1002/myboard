from rest_framework import serializers
from myBoard.categories.models import ExCategories

class ExCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExCategories
        fields = [
            'id',
            'category_name',
            'category_slug',
            'order',
            'sticky',
            'created_at',
            'updated_at',
            'created_by',
            'updated_by',
        ]
