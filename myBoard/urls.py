from django.urls import path, include
from myBoard.core import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path(r'api/', include('myBoard.core.urls')),
    path(r'api/', include('myBoard.s3.urls')),
    path(r'api/', include('myBoard.setting.urls')),
    path(r'api/', include('myBoard.notes.urls')),
    path(r'api/', include('myBoard.moneyExchange.urls')),
]
