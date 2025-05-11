from rest_framework import serializers
from .models import (
    MedicalCenter, Medicine, Stock,
    MedicineReceipt, WeeklyConsumptionReport
)


class MedicalCenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalCenter
        fields = ['id', 'name']


class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = ['id', 'name', 'unit']


class StockSerializer(serializers.ModelSerializer):
    center_name = serializers.CharField(source='center.name', read_only=True)
    medicine_name = serializers.CharField(source='medicine.name', read_only=True)

    class Meta:
        model = Stock
        fields = [
            'id', 'center', 'center_name',
            'medicine', 'medicine_name',
            'quantity', 'last_updated'
        ]


class MedicineReceiptSerializer(serializers.ModelSerializer):
    center_name = serializers.CharField(source='center.name', read_only=True)
    medicine_name = serializers.CharField(source='medicine.name', read_only=True)

    class Meta:
        model = MedicineReceipt
        fields = [
            'id', 'center', 'center_name',
            'medicine', 'medicine_name',
            'quantity_received', 'received_date'
        ]


class WeeklyConsumptionReportSerializer(serializers.ModelSerializer):
    center_name = serializers.CharField(source='center.name', read_only=True)
    medicine_name = serializers.CharField(source='medicine.name', read_only=True)

    class Meta:
        model = WeeklyConsumptionReport
        fields = [
            'id', 'center', 'center_name',
            'medicine', 'medicine_name',
            'week_start', 'week_end',
            'quantity_used', 'observation'
        ]
        read_only_fields = ['observation']
