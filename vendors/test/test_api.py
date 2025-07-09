import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from vendors.models import Vendor

import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from vendors.models import Vendor

@pytest.mark.django_db
def test_create_vendor():
    user = User.objects.create_user(username='testuser', password='testpass')
    token = Token.objects.create(user=user)

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    data = {
        "name": "Test Vendor",
        "contact_details": "test@example.com",
        "address": "123 Street",
        "vendor_code": "TV001"
    }

    response = client.post('/api/vendors/', data, format='json')
    assert response.status_code == 201
    assert Vendor.objects.filter(name="Test Vendor").exists()
