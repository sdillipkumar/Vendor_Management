"""URL configuration for the vendor management system."""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from rest_framework.routers import DefaultRouter
from vendors.views import VendorViewSet
from purchase_orders.views import PurchaseOrderViewSet
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from vendors.views import dashboard_view,vendor_list_view
from django.conf.urls.static import static
from vendors import views
from vendors.views import home_view

router = DefaultRouter()

schema_view = get_schema_view(
    openapi.Info(
        title="Vendor Management API",
        default_version='v1',
        description="API documentation for the Vendor Management System",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home_view, name='home'),
    path('dashboard', dashboard_view, name='dashboard'),
    
    # HTML views
    path('vendors-ui/', views.vendor_list_view, name='vendor_list'),

    # API views
    path('api/vendors/', include('vendors.urls')),
    path('api/orders/', include('purchase_orders.urls')),

    path('api-token-auth/', obtain_auth_token),

    # Swagger & ReDoc
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


