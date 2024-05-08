from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

class Vendor(models.Model):
    name = models.CharField(max_length=100)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class PurchaseOrder(models.Model):
    PENDING = 'Pending'
    COMPLETED = 'Completed'
    CANCELED = 'Canceled'
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (COMPLETED, 'Completed'),
        (CANCELED, 'Canceled'),
    ]

    po_number = models.CharField(max_length=100, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='purchase_orders')
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default=PENDING)
    quality_rating = models.FloatField(null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(5)])
    issue_date = models.DateTimeField(auto_now_add=True)
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    @property
    def is_completed(self):
        return self.status == self.COMPLETED

    @property
    def status_changed(self):
        return self.pk and self.status != self.__class__.objects.get(pk=self.pk).status

    def save(self, *args, **kwargs):
        if self.status_changed and self.status == self.COMPLETED:
            self.acknowledge()
        super().save(*args, **kwargs)

    def acknowledge(self):
        self.acknowledgment_date = timezone.now()

    class Meta:
        ordering = ['-order_date']

class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='historical_performances')
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

    def __str__(self):
        return f"{self.vendor.name} - {self.date}"
