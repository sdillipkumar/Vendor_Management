from django.contrib import admin
from django.contrib import admin
from .models import PurchaseOrder

# Register your models here.

@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ('po_number', 'vendor', 'status', 'issue_date', 'delivery_date', 'acknowledgment_date')
    search_fields = ('po_number', 'vendor__name')
    list_filter = ('status',)
    autocomplete_fields = ['vendor']


