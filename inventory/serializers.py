from rest_framework import serializers
from .models import (
    MedicalCenter, Medicine, Stock,
    MedicineReceipt, WeeklyConsumptionReport, MedicineBatch
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
            'total_quantity', 'last_updated'
        ]

class MedicineBatchSerializer(serializers.ModelSerializer):
    center_name = serializers.CharField(source='center.name', read_only=True)
    medicine_name = serializers.CharField(source='medicine.name', read_only=True)
    is_expired = serializers.BooleanField(read_only=True)
    is_depleted = serializers.BooleanField(read_only=True)
    exp_date = serializers.DateField(format="%d/%m/%Y", required=False)
    received_date = serializers.DateField(format="%d/%m/%Y", required=False)

    class Meta:
        model = MedicineBatch
        fields = [
            'id', 'center', 'center_name',
            'medicine', 'medicine_name',
            'quantity', 'exp_date', 'received_date',
            'batch_code', 'is_expired', 'is_depleted'
        ]


class MedicineReceiptSerializer(serializers.ModelSerializer):
    center_name = serializers.CharField(source='center.name', read_only=True)
    medicine_name = serializers.CharField(source='medicine.name', read_only=True)
    received_date = serializers.DateField(format="%d/%m/%Y", required=False)
    exp_date = serializers.DateField(format="%d/%m/%Y", required=False)

    class Meta:
        model = MedicineReceipt
        fields = [
            'id', 'center', 'center_name',
            'medicine', 'medicine_name',
            'quantity_received', 'received_date', 'exp_date'
        ]


class WeeklyConsumptionReportSerializer(serializers.ModelSerializer):
    center_name = serializers.CharField(source='center.name', read_only=True)
    medicine_name = serializers.CharField(source='medicine.name', read_only=True)
    week_start = serializers.DateField(format="%d/%m/%Y", required=False)
    week_end = serializers.DateField(format="%d/%m/%Y", required=False)

    class Meta:
        model = WeeklyConsumptionReport
        fields = [
            'id', 'center', 'center_name',
            'medicine', 'medicine_name',
            'week_start', 'week_end',
            'quantity_used', 'observation'
        ]
        read_only_fields = ['observation']


class WeeklyReportExcelUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

    def validate_file(self, file):
        if not file.name.endswith('.xlsx'):
            raise serializers.ValidationError("Only .xlsx files are accepted.")
        return file
