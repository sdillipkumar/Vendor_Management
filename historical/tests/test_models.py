import pytest
from vendors.models import Vendor
from historical.models import HistoricalPerformance
from django.utils import timezone

@pytest.mark.django_db
def test_create_historical_record():
    vendor = Vendor.objects.create(
        name="Test Vendor",
        contact_details="Test Contact",
        address="Test Address",
        vendor_code="TV001"
    )

    record = HistoricalPerformance.objects.create(
        vendor=vendor,
        date=timezone.now(),
        on_time_delivery_rate=95.0,
        quality_rating_avg=4.2,
        average_response_time=3.5,
        fulfillment_rate=90.0
    )

    assert HistoricalPerformance.objects.count() == 1
    assert record.vendor == vendor
    assert record.on_time_delivery_rate == 95.0
