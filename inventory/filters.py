from django_filters import rest_framework as filters
from .models import Stock, WeeklyConsumptionReport, MedicineReceipt

class StockFilter(filters.FilterSet):
    medicine_name = filters.CharFilter(field_name='medicine__name', lookup_expr='icontains')
    startDate = filters.DateFilter(field_name='last_updated', lookup_expr='gte')
    endDate = filters.DateFilter(field_name='last_updated', lookup_expr='lte')
    class Meta:
        model = Stock
        fields = ['center', 'medicine', 'startDate', 'endDate']


class WeeklyConsumptionReportFilter(filters.FilterSet):
    week_start = filters.DateFilter(field_name="week_start", lookup_expr='gte')
    week_end = filters.DateFilter(field_name="week_end", lookup_expr='lte')

    class Meta:
        model = WeeklyConsumptionReport
        fields = ['center', 'medicine', 'week_start', 'week_end']

class MedicineReceiptFilter(filters.FilterSet):
    center = filters.NumberFilter(field_name='center__id')
    medicine_name = filters.CharFilter(field_name='medicine__name', lookup_expr='icontains')
    start_date = filters.DateFilter(field_name='received_date', lookup_expr='gte')
    end_date = filters.DateFilter(field_name='received_date', lookup_expr='lte')

    class Meta:
        model = MedicineReceipt
        fields = ['center', 'medicine_name', 'start_date', 'end_date']
