from django.urls import path, include
from myBoard.core import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path(r'api/', include('myBoard.core.urls')),
]
