from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import MedicalCenter, Medicine, Stock, MedicineReceipt, WeeklyConsumptionReport
from .serializers import (
    MedicalCenterSerializer, MedicineSerializer, StockSerializer,
    MedicineReceiptSerializer, WeeklyConsumptionReportSerializer
)
from .filters import StockFilter, WeeklyConsumptionReportFilter


class MedicalCenterViewSet(viewsets.ModelViewSet):
    queryset = MedicalCenter.objects.all()
    serializer_class = MedicalCenterSerializer


class MedicineViewSet(viewsets.ModelViewSet):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.select_related('center', 'medicine').all()
    serializer_class = StockSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = StockFilter


class MedicineReceiptViewSet(viewsets.ModelViewSet):
    queryset = MedicineReceipt.objects.select_related('center', 'medicine').all()
    serializer_class = MedicineReceiptSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['center', 'medicine']


class WeeklyConsumptionReportViewSet(viewsets.ModelViewSet):
    queryset = WeeklyConsumptionReport.objects.select_related('center', 'medicine').all()
    serializer_class = WeeklyConsumptionReportSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = WeeklyConsumptionReportFilter
    search_fields = ['medicine__name']
