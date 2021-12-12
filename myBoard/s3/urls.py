from django.urls import path
from myBoard.s3.views import s3_views
from myBoard.s3.views import s3_folder_views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('s3-bucket/', s3_views.S3Bucket.as_view(), name='s3_bucket'),
    path('get-s3-object/', s3_views.GetS3Object.as_view(), name='get_s3_object'),
    path('set-s3-public-access/', s3_views.SetS3BucketPublicAccess.as_view(), name='set-s3-public-access'),
    path('s3-upload-single/', s3_views.S3UploadSingle.as_view(), name='s3_upload_single'),
    path('s3-upload-multiple/', s3_views.S3UploadMultiple.as_view(), name='s3_upload_multiple'),
    path('s3-folder/', s3_folder_views.S3Folder.as_view(), name='s3_folder'),
    path('s3-file/', s3_folder_views.S3File.as_view(), name='s3_folder'),
    path('s3-object-by-folder/', s3_folder_views.S3GetListFileByFolder.as_view(), name='s3_obj_by_folder'),
]
