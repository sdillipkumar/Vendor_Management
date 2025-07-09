from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,viewsets
from django.shortcuts import get_object_or_404
from .models import PurchaseOrder
from .serializers import PurchaseOrderSerializer
from rest_framework.decorators import action
from django.utils import timezone
from vendors.models import Vendor
from purchase_orders.performance import update_average_response_time
from purchase_orders.forms import PurchaseOrderForm
from django.db.models import Sum
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.timezone import now
from datetime import timedelta
from django.shortcuts import redirect
# Create your views here.

def purchase_order_list_view(request):
    """Render the purchase order list view."""
    # Fetch all purchase orders for the dashboard
    purchase_orders = PurchaseOrder.objects.all().order_by('-issue_date')
    total_orders = PurchaseOrder.objects.count()
    pending_orders = PurchaseOrder.objects.filter(status='PENDING').count()
    completed_orders = PurchaseOrder.objects.filter(status='COMPLETED').count()
    total_value = PurchaseOrder.objects.aggregate(total=Sum('total_amount'))['total'] or 0
    paginator = Paginator(purchase_orders, 5)  # 5 orders per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    statuses = PurchaseOrder.objects.values_list('status', flat=True).distinct()
    # filter logic
    # Get filter values
    status_filter = request.GET.get('status')
    vendor_filter = request.GET.get('vendor')

    # Base queryset
    purchase_orders = PurchaseOrder.objects.all()

    if status_filter:
        purchase_orders = purchase_orders.filter(status=status_filter)
    if vendor_filter:
        purchase_orders = purchase_orders.filter(vendor_id=vendor_filter)

    # Stats
    total_orders = purchase_orders.count()
    pending_orders = purchase_orders.filter(status='Pending').count()
    completed_orders = purchase_orders.filter(status='Completed').count()
    total_value = purchase_orders.aggregate(Sum('total_amount'))['total_amount__sum'] or 0

    context = {
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'completed_orders': completed_orders,
        'total_value': total_value,
        'purchase_orders': purchase_orders,  # for your table
        'statuses': PurchaseOrder.objects.values_list('status', flat=True).distinct(),
        'vendors': Vendor.objects.all(),
        
    }

    # Calculate percentage change in total value
    today = now().date()
    this_month_start = today.replace(day=1)
    last_month_end = this_month_start - timedelta(days=1)
    last_month_start = last_month_end.replace(day=1)

    this_month_orders = PurchaseOrder.objects.filter(issue_date__gte=this_month_start)
    last_month_orders = PurchaseOrder.objects.filter(issue_date__range=(last_month_start, last_month_end))

    this_month_count = this_month_orders.count()
    last_month_count = last_month_orders.count()

    if last_month_count > 0:
        percentage_change = ((this_month_count - last_month_count) / last_month_count) * 100
    else:
        percentage_change = 100 if this_month_count > 0 else 0

    
    return render(request, 'dashboard/purchase_order_list.html', context)

class PurchaseOrderListCreateView(APIView):
    def get(self, request):
        vendor_id = request.query_params.get('vendor')
        if vendor_id:
            pos = PurchaseOrder.objects.filter(vendor_id=vendor_id)
        else:
            pos = PurchaseOrder.objects.all()
        serializer = PurchaseOrderSerializer(pos, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PurchaseOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PurchaseOrderDetailView(APIView):
    def get(self, request, po_id):
        po = get_object_or_404(PurchaseOrder, id=po_id)
        serializer = PurchaseOrderSerializer(po)
        return Response(serializer.data)

    def put(self, request, po_id):
        po = get_object_or_404(PurchaseOrder, id=po_id)
        serializer = PurchaseOrderSerializer(po, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, po_id):
        po = get_object_or_404(PurchaseOrder, id=po_id)
        po.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PurchaseOrderAcknowledgeView(APIView):
    def post(self, request, po_id):
        po = get_object_or_404(PurchaseOrder, id=po_id)
        po.acknowledgment_date = request.data.get("acknowledgment_date")
        po.save()
        return Response({"message": "Acknowledgment date updated."})


class PurchaseOrderViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

    @action(detail=True, methods=['post'])
    def acknowledge(self, request, pk=None):
        try:
            po = self.get_object()

            if po.acknowledgment_date:
                return Response({'detail': 'Already acknowledged'}, status=status.HTTP_400_BAD_REQUEST)

            po.acknowledgment_date = timezone.now()
            po.save()

            update_average_response_time(po.vendor)

            return Response({'detail': 'Acknowledged successfully'}, status=status.HTTP_200_OK)

        except PurchaseOrder.DoesNotExist:
            return Response({'detail': 'Purchase Order not found'}, status=status.HTTP_404_NOT_FOUND)
        
def create_purchase_order_form(request):
    if request.method == 'POST':
        form = PurchaseOrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('purchase_order_list')  # Create this later
    else:
        form = PurchaseOrderForm()
    return render(request, 'dashboard/po_create.html', {'form': form})    


# # View to handle purchase order detail
# This view will render the purchase order detail page.    
def purchase_order_detail(request, pk):
    order = get_object_or_404(PurchaseOrder, pk=pk)
    return render(request, 'dashboard/purchase_order_detail.html', {'order': order})