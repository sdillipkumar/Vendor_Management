from django.urls import path
from .views import (
    PurchaseOrderListCreateView,
    PurchaseOrderDetailView,
    PurchaseOrderAcknowledgeView
)
from . import views
from .views import create_purchase_order_form, PurchaseOrderListCreateView
urlpatterns = [
    # 🟩 Form-based HTML UI
    path('create-ui/', create_purchase_order_form, name='create_purchase_order_ui'),  # UI view for creating a purchase order
    path('orders-ui/', views.purchase_order_list_view, name='purchase_order_list'),   # UI view for listing purchase orders
    path('purchase_orders/<int:pk>/', views.purchase_order_detail, name='po-detail'),  # ✅ HTML detail view
    # 🟦 API Endpoints
    path('purchase_orders/', views.PurchaseOrderListCreateView.as_view(), name='po-list-create'),  # API for list & create
    # 🟦 API Endpoints for individual purchase orders
    path('po/<int:po_id>/', views.PurchaseOrderDetailView.as_view(), name='po-detail-api'),  # ✅ API detail view
    path('purchase_orders/<int:po_id>/acknowledge/', views.PurchaseOrderAcknowledgeView.as_view(), name='po-acknowledge'),  # API to acknowledge
]