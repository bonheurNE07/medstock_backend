from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    MedicalCenterViewSet, MedicineViewSet, StockViewSet,
    MedicineReceiptViewSet, WeeklyConsumptionReportViewSet,
    WeeklyReportExcelUploadView, MedicineReceiptExcelUploadView
)

router = DefaultRouter()
router.register(r'centers', MedicalCenterViewSet)
router.register(r'medicines', MedicineViewSet)
router.register(r'stocks', StockViewSet)
router.register(r'receipts', MedicineReceiptViewSet)
router.register(r'weekly-reports', WeeklyConsumptionReportViewSet)

urlpatterns = router.urls + [
    path('weekly-reports/upload/', WeeklyReportExcelUploadView.as_view(), name='weeklyreport-upload'),
    path('receipts/upload/', MedicineReceiptExcelUploadView.as_view(), name='receipts-upload'),
]
