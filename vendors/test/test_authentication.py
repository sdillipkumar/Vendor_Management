import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

"""This test suite includes:

✅1. Authenticated Vendor Creation – Ensures that a valid token allows creation.

❌ Unauthenticated Vendor Creation – Confirms 401 Unauthorized if no token is used."""

@pytest.mark.django_db
def test_authenticated_vendor_creation():
    user = User.objects.create_user(username='testuser', password='testpass')
    token, _ = Token.objects.get_or_create(user=user)

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    data = {
        "name": "Test Vendor",
        "contact_details": "Test Contact",
        "address": "123 Street",
        "vendor_code": "VEND123"
    }

    response = client.post("/api/vendors/", data, format='json')
    assert response.status_code == 201

@pytest.mark.django_db
def test_unauthenticated_vendor_creation():
    client = APIClient()

    data = {
        "name": "Unauthorized Vendor",
        "contact_details": "No Auth",
        "address": "No Address",
        "vendor_code": "NOAUTH"
    }

    response = client.post("/api/vendors/", data, format='json')
    assert response.status_code == 401

""" ✅ 2.  test for token generation via login"""
@pytest.mark.django_db
def test_obtain_auth_token():
    user = User.objects.create_user(username='testuser', password='testpass123')
    client = APIClient()
    response = client.post('/api-token-auth/', {'username': 'testuser', 'password': 'testpass123'})
    assert response.status_code == 200
    assert 'token' in response.data

"""✅ 3. Test protected endpoint (e.g., creating a purchase order)"""
@pytest.mark.django_db
def test_create_purchase_order_authenticated():
    user = User.objects.create_user(username='authuser', password='secret123')
    token = Token.objects.create(user=user)

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    # Set up a vendor before creating a PO
    from vendors.models import Vendor
    vendor = Vendor.objects.create(
        name="Test Vendor",
        contact_details="Test Contact",
        address="123 Test Lane",
        vendor_code="TV123"
    )

    data = {
        "po_number": "PO2001",
        "vendor": vendor.id,
        "order_date": "2025-06-10T10:00:00Z",
        "delivery_date": "2025-06-15T10:00:00Z",
        "items": [{"item": "Widget", "quantity": 10}],
        "quantity": 10,
        "status": "pending",
        "issue_date": "2025-06-10T10:00:00Z"
    }

    response = client.post("/api/purchase_orders/", data, format='json')
    assert response.status_code == 201

""" 2. Test Token Reuse
Once token is obtained, you can reuse it to access protected endpoints:"""

@pytest.mark.django_db
def test_token_reuse_allows_access():
    user = User.objects.create_user(username='reuseuser', password='pass123')
    token = Token.objects.create(user=user)

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    response = client.get("/api/vendors/")
    assert response.status_code == 200 or response.status_code == 204  # depending on data
    