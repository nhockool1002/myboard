from django.urls import path
from myBoard.paymentReminder.views import MyBoardPaymentReminderAPI
urlpatterns = [
    path('payment-reminder/', MyBoardPaymentReminderAPI.as_view(), name='paymentReminder'),
    path('payment-reminder/<int:id>', MyBoardPaymentReminderAPI.as_view(), name='paymentReminder_update'),
]
