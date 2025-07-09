from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PurchaseOrder
from vendors.models import Vendor
from django.db.models import F, Avg, Count, ExpressionWrapper, DurationField
from django.utils.timezone import now
from vendors.utils import create_historical_record

# Signal to update vendor performance metrics after a Purchase Order is saved

@receiver(post_save, sender=PurchaseOrder)
def update_vendor_performance(sender, instance, created, **kwargs):
    vendor = instance.vendor
    pos = PurchaseOrder.objects.filter(vendor=vendor)

    # 1. On-Time Delivery Rate
    completed_pos = pos.filter(status='completed')
    if completed_pos.exists():
        on_time_count = completed_pos.filter(delivery_date__lte=F('order_date')).count()
        vendor.on_time_delivery_rate = round((on_time_count / completed_pos.count()) * 100, 2)
    else:
        vendor.on_time_delivery_rate = 0.0

    # 2. Quality Rating Average (for completed POs with rating)
    rated_pos = completed_pos.exclude(quality_rating__isnull=True)
    if rated_pos.exists():
        avg_quality = rated_pos.aggregate(avg=Avg('quality_rating'))['avg']
        vendor.quality_rating_avg = round(avg_quality, 2)
    else:
        vendor.quality_rating_avg = 0.0

    # 3. Average Response Time (for acknowledged POs)
    acknowledged_pos = pos.filter(acknowledgment_date__isnull=False)
    if acknowledged_pos.exists():
        diff_expr = ExpressionWrapper(
            F('acknowledgment_date') - F('issue_date'),
            output_field=DurationField()
        )
        avg_response_time = acknowledged_pos.annotate(response_diff=diff_expr).aggregate(
            avg=Avg('response_diff')
        )['avg']
        vendor.average_response_time = round(avg_response_time.total_seconds() / 3600, 2)  # in hours
    else:
        vendor.average_response_time = 0.0

    # 4. Fulfillment Rate (based on POs with status 'completed')
    total_issued = pos.count()
    if total_issued > 0:
        fulfilled_count = completed_pos.count()
        vendor.fulfillment_rate = round((fulfilled_count / total_issued) * 100, 2)
    else:
        vendor.fulfillment_rate = 0.0

    vendor.save()
    # Create a historical record for the vendor performance update
    create_historical_record(vendor)

