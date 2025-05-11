import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, filters, status
from rest_framework.parsers import MultiPartParser
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.dateparse import parse_date
from .models import MedicalCenter, Medicine, Stock, MedicineReceipt, WeeklyConsumptionReport
from .serializers import (
    MedicalCenterSerializer, MedicineSerializer, StockSerializer,
    MedicineReceiptSerializer, WeeklyConsumptionReportSerializer,
    WeeklyReportExcelUploadSerializer,
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

class WeeklyReportExcelUploadView(APIView):
    def post(self, request):
        serializer = WeeklyReportExcelUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        file = serializer.validated_data['file']

        df = pd.read_excel(file)

        required_columns = ['week_start', 'week_end', 'center', 'medicine', 'quantity_received', 'quantity_used']
        for col in required_columns:
            if col not in df.columns:
                return Response({"error": f"Missing column: {col}"}, status=400)

        success_count = 0
        errors = []

        for index, row in df.iterrows():
            try:
                center = MedicalCenter.objects.get(name=row['center'])
                medicine = Medicine.objects.get(name=row['medicine'])

                report = WeeklyConsumptionReport.objects.create(
                    week_start=parse_date(str(row['week_start'])),
                    week_end=parse_date(str(row['week_end'])),
                    center=center,
                    medicine=medicine,
                    quantity_received=int(row['quantity_received']),
                    quantity_used=int(row['quantity_used'])
                )
                success_count += 1
            except Exception as e:
                errors.append({"row": index + 2, "error": str(e)})

        return Response({
            "inserted": success_count,
            "errors": errors
        }, status=status.HTTP_200_OK)

class MedicineReceiptExcelUploadView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        file_obj = request.FILES.get('file')
        if not file_obj:
            return Response({"error": "No file provided."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            df = pd.read_excel(file_obj)
        except Exception as e:
            return Response({"error": f"Invalid Excel file. Details: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        required_columns = ['Centre', 'Nom du Médicament', 'Unité', 'Quantité Reçue', 'Date de Réception']
        if not all(col in df.columns for col in required_columns):
            return Response({"error": "Excel file must contain these columns: " + ", ".join(required_columns)}, status=status.HTTP_400_BAD_REQUEST)

        receipts_created = []

        for _, row in df.iterrows():
            try:
                center_name = row['Centre']
                medicine_name = row['Nom du Médicament']
                unit = row['Unité']
                quantity = int(row['Quantité Reçue'])
                date_received = parse_date(str(row['Date de Réception']))

                center, _ = MedicalCenter.objects.get_or_create(name=center_name)
                medicine, _ = Medicine.objects.get_or_create(name=medicine_name, defaults={'unit': unit})

                receipt = MedicineReceipt.objects.create(
                    center=center,
                    medicine=medicine,
                    quantity_received=quantity,
                    date_received=date_received
                )

                receipts_created.append(receipt.id)

            except Exception as e:
                return Response({"error": f"Error processing row: {row.to_dict()}. Details: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": f"Successfully created {len(receipts_created)} medicine receipts."}, status=status.HTTP_201_CREATED)