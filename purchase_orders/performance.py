# purchase_orders/performance.py

from django.db.models import F, ExpressionWrapper, DurationField, Avg
from purchase_orders.models import PurchaseOrder

def update_average_response_time(vendor):
    acknowledged_orders = PurchaseOrder.objects.filter(
        vendor=vendor,
        issue_date__isnull=False,
        acknowledgment_date__isnull=False
    ).annotate(
        response_time=ExpressionWrapper(
            F('acknowledgment_date') - F('issue_date'),
            output_field=DurationField()
        )
    )

    avg_response = acknowledged_orders.aggregate(avg=Avg('response_time'))['avg']
    
    if avg_response:
        vendor.average_response_time = avg_response.total_seconds() / 3600  # hours
        vendor.save()
