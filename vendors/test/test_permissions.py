import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User, Group
from rest_framework.authtoken.models import Token
from django.urls import reverse

from vendors.models import Vendor

"""
Admins can create and view vendors ✅

Vendors cannot create new vendors ❌

Unauthenticated users are blocked ❌

"""

@pytest.fixture
def admin_user(db):
    user = User.objects.create_user(username="admin_user", password="adminpass")
    group, _ = Group.objects.get_or_create(name='Admin')
    user.groups.add(group)
    token, _ = Token.objects.get_or_create(user=user)
    return user, token


@pytest.fixture
def vendor_user(db):
    user = User.objects.create_user(username="vendor_user", password="vendorpass")
    group, _ = Group.objects.get_or_create(name='Vendor')
    user.groups.add(group)
    token, _ = Token.objects.get_or_create(user=user)
    return user, token


@pytest.fixture
def api_client():
    return APIClient()


def test_admin_can_create_vendor(api_client, admin_user):
    user, token = admin_user
    api_client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
    data = {
        "name": "Test Vendor",
        "contact_details": "test@example.com",
        "address": "Test City",
        "vendor_code": "TEST123"
    }
    response = api_client.post("/api/vendors/", data, format='json')
    assert response.status_code == 201


def test_vendor_cannot_create_vendor(api_client, vendor_user):
    user, token = vendor_user
    api_client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
    data = {
        "name": "Illegal Vendor",
        "contact_details": "nope@example.com",
        "address": "Nowhere",
        "vendor_code": "ILLEGAL"
    }
    response = api_client.post("/api/vendors/", data, format='json')
    assert response.status_code in [403, 401]  # Forbidden or Unauthorized


def test_unauthenticated_cannot_access(api_client):
    response = api_client.get("/api/vendors/")
    assert response.status_code == 401  # Unauthorized


def test_admin_can_view_all_vendors(api_client, admin_user):
    user, token = admin_user
    api_client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
    response = api_client.get("/api/vendors/")
    assert response.status_code == 200
