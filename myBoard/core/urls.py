from django.urls import path
from myBoard.core import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
  path('hello/', views.HelloView.as_view(), name='hello'),
  path('api-token-auth/', views.CustomAuthToken.as_view(), name='api_token_auth'),
]
