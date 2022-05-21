from django.urls import path
from myBoard.license.views import LicenseAPI
urlpatterns = [
    path('license/', LicenseAPI.as_view(), name='license'),
]
