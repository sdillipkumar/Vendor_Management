from django.contrib import admin
from django.contrib import admin
from .models import Vendor

# Register your models here.

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('name', 'vendor_code', 'on_time_delivery_rate', 'quality_rating_avg')
    search_fields = ('name', 'vendor_code')
    list_filter = ('on_time_delivery_rate',)
    ordering = ('name',)


