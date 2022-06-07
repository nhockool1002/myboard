from django.urls import path
from myBoard.moneyExchange.views import MoneyExchangeAPI, HistoricalMoneyAPI
urlpatterns = [
    path('money-exchange/', MoneyExchangeAPI.as_view(), name='money_exchange'),
    path('historical-exchange/', HistoricalMoneyAPI.as_view(), name='money_exchange'),
]
