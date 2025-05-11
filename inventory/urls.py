from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    MedicalCenterViewSet, MedicineViewSet, StockViewSet,
    MedicineReceiptViewSet, WeeklyConsumptionReportViewSet,
    WeeklyReportExcelUploadView, MedicineReceiptExcelUploadView,
    WeeklyReportExcelExportView,DashboardAnalyticsView,
    DashboardAnalyticsView,
)

router = DefaultRouter()
router.register(r'centers', MedicalCenterViewSet)
router.register(r'medicines', MedicineViewSet)
router.register(r'stocks', StockViewSet)
router.register(r'receipts', MedicineReceiptViewSet)
router.register(r'weekly-reports', WeeklyConsumptionReportViewSet)

urlpatterns = router.urls + [
    path('reports/upload/', WeeklyReportExcelUploadView.as_view(), name='weeklyreport-upload'),
    path('reports/export/', WeeklyReportExcelExportView.as_view(), name='weeklyreports-export'),
    path('receipts/upload/', MedicineReceiptExcelUploadView.as_view(), name='receipts'),
    path('dashboard/', DashboardAnalyticsView.as_view(), name='dashboard-analytics'),
]
