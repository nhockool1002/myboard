from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.views import status
from django.urls import path
import requests
import os

# Create your tests here.


class TestCoreApi(APITestCase):
    def setUp(self) -> None:
        self.url = reverse('api_token_auth')

        User.objects.create_superuser(
            username="admin", email="admin@qa.team", password="abc123")

    def test_send_valid_infomation_to_get_token(self):
        data = {
            "username": "admin",
            "password": "abc123"
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
