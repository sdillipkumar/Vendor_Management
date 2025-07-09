from django import forms
from .models import PurchaseOrder

class PurchaseOrderForm(forms.ModelForm):
    class Meta:
        model = PurchaseOrder
        fields = [
            'po_number', 'vendor', 'order_date', 'delivery_date',
            'items', 'quantity', 'status', 'issue_date', 'acknowledgment_date'
        ]
        widgets = {
            'po_number': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg dark:bg-gray-700 dark:text-white'
            }),
            'vendor': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg dark:bg-gray-700 dark:text-white'
            }),
            'items': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg dark:bg-gray-700 dark:text-white',
                'rows': 3
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg dark:bg-gray-700 dark:text-white'
            }),
            'status': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg dark:bg-gray-700 dark:text-white'
            }),
            'order_date': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'w-full px-4 py-2 border rounded-lg dark:bg-gray-700 dark:text-white'
            }),
            'delivery_date': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'w-full px-4 py-2 border rounded-lg dark:bg-gray-700 dark:text-white'
            }),
            'issue_date': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'w-full px-4 py-2 border rounded-lg dark:bg-gray-700 dark:text-white'
            }),
            'acknowledgment_date': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'w-full px-4 py-2 border rounded-lg dark:bg-gray-700 dark:text-white'
            }),
        }
