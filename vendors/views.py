from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Vendor
from .serializers import VendorSerializer
from rest_framework import viewsets, status
from rest_framework.decorators import action
from django.utils import timezone
from purchase_orders.performance import update_average_response_time
from purchase_orders.models import PurchaseOrder
from vendors.serializers import VendorSerializer
from purchase_orders.serializers import PurchaseOrderSerializer
from purchase_orders.models import PurchaseOrder
from vendors.permissions import IsVendor
from rest_framework.permissions import IsAuthenticated
from vendors.permissions import IsAdmin, IsAdminOrVendor
from django.db.models import Avg
from purchase_orders.models import PurchaseOrder
from django.db.models import Count, Sum, F
from vendors.utils import get_vendor_metrics  # Example utility function for historical data
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.core.paginator import Paginator

def home_view(request):
    return render(request, 'home.html')


# Dashboard view to display vendor and purchase order statistics
def dashboard_view(request):
    total_vendors = Vendor.objects.count()
    total_purchase_orders = PurchaseOrder.objects.count()
    pending_orders = PurchaseOrder.objects.filter(status="PENDING").count()

    # Use one of the correct fields
    average_rating = Vendor.objects.aggregate(avg_rating=Avg('on_time_delivery_rate'))['avg_rating'] or 0

    recent_orders = PurchaseOrder.objects.select_related('vendor').order_by('-issue_date')[:5]

    # Get top vendors by on_time_delivery_rate
    top_vendors = Vendor.objects.order_by('-on_time_delivery_rate')[:5]
    vendor_names = [vendor.name for vendor in top_vendors]
    performance_scores = [round(v.on_time_delivery_rate or 0, 2) for v in top_vendors]

    return render(request, 'dashboard/dashboard.html', {
        'total_vendors': total_vendors,
        'total_purchase_orders': total_purchase_orders,
        'pending_orders': pending_orders,
        'average_rating': average_rating,
        'recent_orders': recent_orders,
        'vendor_names': vendor_names,
        'performance_scores': performance_scores,
    })

def vendor_detail(request, pk):
    vendor = get_object_or_404(Vendor, pk=pk)
    return render(request, 'dashboard/vendor_detail.html', {'vendor': vendor})


def vendor_list_view(request):
    vendors = Vendor.objects.all()
    search_query = request.GET.get('search', '')
    category = request.GET.get('category') or 'All'  # ensures fallback to 'All'
    if not category:
        category = 'All'
    
    print(f"AJAX call received - Search: {search_query}, Category: {category}")

    if search_query:
        vendors = vendors.filter(name__icontains=search_query)
    if category != 'All':
        vendors = vendors.filter(category__iexact=category)  
    paginator = Paginator(vendors, 6)  # 6 vendors per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('dashboard/_vendor_cards.html', {
            'vendors': page_obj,  # Used paginated vendors
            'page_obj': page_obj,
        }, request=request)
        return JsonResponse({'html': html})     
    
    context = {
        'vendors': page_obj,
        'search_query': search_query,
        'selected_category': category,
        'categories': ['All', 'Suppliers', 'Services', 'Contractors'],
        'page_obj': page_obj
    }    
    return render(request, 'dashboard/vendor_list.html',context)


def vendor_performance(request, vendor_id):
    vendor = get_object_or_404(Vendor, id=vendor_id)
    metrics = get_vendor_metrics(vendor) 
    vendor.quality_rating_percent = vendor.quality_rating_avg * 20
     
    return render(request, 'dashboard/_vendor_performance.html', {
        'vendor': vendor,
        'metrics': metrics,
    })

































 #  used DRF's APIView to create views for handling vendor data

class VendorListCreateView(APIView):
    def get(self, request):
        vendors = Vendor.objects.all()
        serializer = VendorSerializer(vendors, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VendorDetailView(APIView):
    def get(self, request, vendor_id):
        vendor = get_object_or_404(Vendor, id=vendor_id)
        serializer = VendorSerializer(vendor)
        return Response(serializer.data)

    def put(self, request, vendor_id):
        vendor = get_object_or_404(Vendor, id=vendor_id)
        serializer = VendorSerializer(vendor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, vendor_id):
        vendor = get_object_or_404(Vendor, id=vendor_id)
        vendor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class VendorPerformanceView(APIView):
    def get(self, request, pk):
        vendor = get_object_or_404(Vendor, pk=pk)
        data = {
            "vendor_id": vendor.id,
            "on_time_delivery_rate": vendor.on_time_delivery_rate,
            "quality_rating_avg": vendor.quality_rating_avg,
            "average_response_time": vendor.average_response_time,
            "fulfillment_rate": vendor.fulfillment_rate,
        }
        return Response(data, status=status.HTTP_200_OK)


class PurchaseOrderViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

    # 👉 Custom action for acknowledgment

    @action(detail=True, methods=['post'])
    def acknowledge(self, request, pk=None):
        try:
            po = self.get_object()

            if po.acknowledgment_date:
                return Response({'detail': 'Already acknowledged'}, status=status.HTTP_400_BAD_REQUEST)

            po.acknowledgment_date = timezone.now()
            po.save()

            # Update vendor's average response time
            update_average_response_time(po.vendor)

            return Response({'detail': 'Acknowledged successfully'}, status=status.HTTP_200_OK)

        except PurchaseOrder.DoesNotExist:
            return Response({'detail': 'Purchase Order not found'}, status=status.HTTP_404_NOT_FOUND)

# This viewset allows vendors to manage their own data
class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    

    def get_permissions(self):
        # POST, PUT, DELETE: Admins only
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return [IsAuthenticated(), IsAdmin()]
        # GET: Admins and Vendors
        return [IsAuthenticated(), IsAdminOrVendor()]