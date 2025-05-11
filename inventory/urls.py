from rest_framework.routers import DefaultRouter
from .views import (
    MedicalCenterViewSet, MedicineViewSet, StockViewSet,
    MedicineReceiptViewSet, WeeklyConsumptionReportViewSet
)

router = DefaultRouter()
router.register(r'centers', MedicalCenterViewSet)
router.register(r'medicines', MedicineViewSet)
router.register(r'stocks', StockViewSet)
router.register(r'receipts', MedicineReceiptViewSet)
router.register(r'weekly-reports', WeeklyConsumptionReportViewSet)

urlpatterns = router.urls
