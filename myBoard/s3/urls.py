from django.urls import path
from myBoard.s3 import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('create-s3-bucket/', views.CreateS3Bucket.as_view(), name='create_s3_bucket'),
    path('get-s3-object/', views.GetS3Object.as_view(), name='get_s3_object'),
]
