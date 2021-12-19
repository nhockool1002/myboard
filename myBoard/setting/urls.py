from django.urls import path
from myBoard.setting.views import SettingsAPI, UpdadteThumbSetting
urlpatterns = [
    path('settings/', SettingsAPI.as_view(), name='settings'),
    path('settings/update-thumb', UpdadteThumbSetting.as_view(), name='update_thumb'),
]
