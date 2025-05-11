from django_filters import rest_framework as filters
from .models import Stock, WeeklyConsumptionReport


class StockFilter(filters.FilterSet):
    class Meta:
        model = Stock
        fields = ['center', 'medicine']


class WeeklyConsumptionReportFilter(filters.FilterSet):
    week_start = filters.DateFilter(field_name="week_start", lookup_expr='gte')
    week_end = filters.DateFilter(field_name="week_end", lookup_expr='lte')

    class Meta:
        model = WeeklyConsumptionReport
        fields = ['center', 'medicine', 'week_start', 'week_end']
