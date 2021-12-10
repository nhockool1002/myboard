from django.urls import path
from myBoard.s3 import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('s3-bucket/', views.S3Bucket.as_view(), name='s3_bucket'),
    path('get-s3-object/', views.GetS3Object.as_view(), name='get_s3_object'),
    path('set-s3-public-access/', views.SetS3BucketPublicAccess.as_view(), name='set-s3-public-access'),
]
