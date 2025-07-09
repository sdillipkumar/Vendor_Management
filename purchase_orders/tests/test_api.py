import pytest
from rest_framework.test import APIClient
from vendors.models import Vendor
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_create_purchase_order():
    user = User.objects.create_user(username='testuser', password='testpass')
    vendor = Vendor.objects.create(
        name="Test Vendor",
        contact_details="123456789",
        address="Test Address",
        vendor_code="VENDOR123"
    )

    client = APIClient()
    client.force_authenticate(user=user)

    data = {
    "po_number": "PO001",
    "vendor": vendor.id,
    "order_date": "2025-06-10T00:00:00Z",   # ISO 8601 format (required for DateTimeField)
    "issue_date": "2025-06-09T12:00:00Z",   # ✅ Add this field
    "delivery_date": "2025-06-15T00:00:00Z",
    "items": ["Item A", "Item B"],
    "quantity": 100,
    "status": "pending"
}

    response = client.post("/api/purchase_orders/", data, format='json')
    print(response.status_code)
    print(response.data)  # This shows why the serializer failed

    assert response.status_code == 201
