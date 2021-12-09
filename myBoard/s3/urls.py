from django.urls import path
from myBoard.s3 import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
  path('s3-init/', views.S3ApiView.as_view(), name='s3_init'),
]
