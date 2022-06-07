from django.db import models

class MyBoardPaymentReminder(models.Model):
    id = models.AutoField(primary_key=True)
    payment_name = models.CharField(max_length=255, blank=True, null=True)
    payment_content = models.TextField(blank=True, null=True)
    payment_due_date = models.DateTimeField(null=True)
    payment_price = models.CharField(max_length=255, blank=True, null=True)
    payment_status = models.BooleanField(null=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=255, blank=True, null=True)
    updated_by = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'myboard_payment_reminder'
