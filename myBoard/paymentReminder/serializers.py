from rest_framework import serializers
from myBoard.paymentReminder.models import MyBoardPaymentReminder

class MyBoardPaymentReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyBoardPaymentReminder
        fields = [
            'id',
            'payment_name',
            'payment_content',
            'payment_due_date',
            'payment_price',
            'payment_status',
            'created_at',
            'updated_at',
            'created_by',
            'updated_by',
        ]
