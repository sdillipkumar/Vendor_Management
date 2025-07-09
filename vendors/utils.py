from historical.models import HistoricalPerformance


# This utility function creates a historical record for a vendor's performance.

def create_historical_record(vendor):
    HistoricalPerformance.objects.create(
        vendor=vendor,
        on_time_delivery_rate=vendor.on_time_delivery_rate,
        quality_rating_avg=vendor.quality_rating_avg,
        average_response_time=vendor.average_response_time,
        fulfillment_rate=vendor.fulfillment_rate
    )

def get_vendor_metrics(vendor):
    # Later you can calculate from PurchaseOrder model
    return [
        {'date': '2025-05', 'delivery_rate': 92, 'quality_rating': 4.8, 'response_time': 3.2, 'fulfillment_rate': 96},
        {'date': '2025-04', 'delivery_rate': 87, 'quality_rating': 4.5, 'response_time': 4.1, 'fulfillment_rate': 92},
        {'date': '2025-03', 'delivery_rate': 90, 'quality_rating': 4.7, 'response_time': 3.6, 'fulfillment_rate': 94},
    ]
