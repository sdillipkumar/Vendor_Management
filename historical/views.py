from django.shortcuts import render
from rest_framework import viewsets
from .models import HistoricalPerformance
from .serializers import HistoricalPerformanceSerializer

# Create your views here.

## HistoricalPerformanceViewSet provides a read-only viewset for the HistoricalPerformance model. 
class HistoricalPerformanceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = HistoricalPerformance.objects.all()
    serializer_class = HistoricalPerformanceSerializer
 