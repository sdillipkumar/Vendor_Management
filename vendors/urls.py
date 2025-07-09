from django.urls import path
from .views import VendorListCreateView, VendorDetailView
from vendors.views import VendorPerformanceView, VendorViewSet
from rest_framework.routers import DefaultRouter
from historical.views import HistoricalPerformanceViewSet
from rest_framework.authtoken.views import obtain_auth_token
from . import views
# Create a router and register the viewsets
router = DefaultRouter()
router.register(r'vendors', VendorViewSet, basename='vendor')
router.register(r'historical-performance', HistoricalPerformanceViewSet, basename='historical-performance')

urlpatterns = [
    path('<int:pk>/', views.vendor_detail, name='vendor_detail'),
    path('vendors/', VendorListCreateView.as_view(), name='vendor-list-create'),
    path('vendors/<int:vendor_id>/performance/', views.vendor_performance, name='vendor_performance'),
    path('vendors/<int:vendor_id>/', VendorDetailView.as_view(), name='vendor-detail'),
    path('api-token-auth/', obtain_auth_token),
    path('vendors/<int:pk>/performance/', VendorPerformanceView.as_view(), name='vendor-performance'),

]