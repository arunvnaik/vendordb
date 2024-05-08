from django.db.models import Avg
from vendor_app.models import PurchaseOrder

def update_on_time_delivery_rate(vendor):
    completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status='Completed')
    on_time_delivered_pos = completed_pos.filter(delivery_date__lte=F('delivery_date')).count()
    total_completed_pos = completed_pos.count()
    if total_completed_pos > 0:
        on_time_delivery_rate = on_time_delivered_pos / total_completed_pos * 100
        vendor.on_time_delivery_rate = on_time_delivery_rate
        vendor.save()

def update_quality_rating_avg(vendor):
    completed_pos_with_rating = PurchaseOrder.objects.filter(vendor=vendor, status='Completed', quality_rating__isnull=False)
    quality_rating_avg = completed_pos_with_rating.aggregate(avg_rating=Avg('quality_rating'))['avg_rating']
    if quality_rating_avg is not None:
        vendor.quality_rating_avg = quality_rating_avg
        vendor.save()

def update_average_response_time(vendor):
    acknowledged_pos = PurchaseOrder.objects.filter(vendor=vendor, acknowledgment_date__isnull=False)
    response_times = [(po.acknowledgment_date - po.issue_date).total_seconds() / 3600 for po in acknowledged_pos]
    if response_times:
        average_response_time = sum(response_times) / len(response_times)
        vendor.average_response_time = average_response_time
        vendor.save()

def update_fulfillment_rate(vendor):
    total_pos = PurchaseOrder.objects.filter(vendor=vendor)
    successful_pos = total_pos.filter(status='Completed', issue_date__isnull=False, acknowledgment_date__isnull=False)
    fulfillment_rate = successful_pos.count() / total_pos.count() * 100
    vendor.fulfillment_rate = fulfillment_rate
    vendor.save()
