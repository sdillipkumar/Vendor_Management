from django.db import models

# Create your models here.
class Vendor(models.Model):
    CATEGORY_CHOICES = [
        ('Suppliers', 'Suppliers'),
        ('Services', 'Services'),
        ('Contractors', 'Contractors'),
    ]
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Suppliers')
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=100, unique=True)
    logo = models.ImageField(upload_to='vendor_logos/', blank=True, null=True)
    on_time_delivery_rate = models.FloatField(default=0.0)
    quality_rating_avg = models.FloatField(default=0.0)
    average_response_time = models.FloatField(default=0.0)
    fulfillment_rate = models.FloatField(default=0.0)

    def get_logo_url(self):
        if self.logo and hasattr(self.logo, 'url'):
            return self.logo.url
        return 'https://via.placeholder.com/40'

    def __str__(self):
        return self.name