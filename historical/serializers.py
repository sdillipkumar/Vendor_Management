from rest_framework import serializers
from historical.models import HistoricalPerformance

class HistoricalPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricalPerformance
        fields = '__all__'
