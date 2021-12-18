from django.urls import path
from myBoard.setting.views import SettingsAPI
urlpatterns = [
    path('settings/', SettingsAPI.as_view(), name='settings'),
]
