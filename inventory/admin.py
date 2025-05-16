from django.contrib import admin
from .models import MedicalCenter, Medicine, Stock, MedicineReceipt, WeeklyConsumptionReport, MedicineBatch


@admin.register(MedicalCenter)
class MedicalCenterAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ['name', 'unit']
    search_fields = ['name', 'unit']

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ['center', 'medicine', 'total_quantity', 'last_updated']
    list_filter = ['center', 'medicine']
    search_fields = ['center__name', 'medicine__name']
    readonly_fields = ['last_updated']
    fieldsets = (
        ("Stock Info", {
            "fields": ("center", "medicine", "total_quantity")
        }),
        ("Meta", {
            "fields": ("last_updated",),
            "classes": ("collapse",)
        }),
    )

@admin.register(MedicineReceipt)
class MedicineReceiptAdmin(admin.ModelAdmin):
    list_display = ['center', 'medicine', 'quantity_received', 'received_date', 'exp_date']
    list_filter = ['center', 'medicine', 'received_date']
    search_fields = ['center__name', 'medicine__name']
    fieldsets = (
        ("Reception Info", {
            "fields": ("center", "medicine", "quantity_received")
        }),
        ("Date", {
            "fields": ("received_date","exp_date",),
        }),
    )

@admin.register(MedicineBatch)
class MedicineBatchAdmin(admin.ModelAdmin):
    list_display = ['center', 'medicine', 'quantity', 'exp_date', 'received_date', 'batch_code']
    list_filter = ['center', 'medicine', 'received_date']
    search_fields = ['center__name', 'medicine__name']
    fieldsets = (
        ("Reception Info", {
            "fields": ("center", "medicine", "quantity_received", "batch_code")
        }),
        ("Date", {
            "fields": ("received_date","exp_date",),
        }),
    )

@admin.register(WeeklyConsumptionReport)
class WeeklyConsumptionReportAdmin(admin.ModelAdmin):
    list_display = ['center', 'medicine', 'week_start', 'week_end', 'quantity_used', 'observation']
    list_filter = ['center', 'medicine', 'week_start']
    search_fields = ['center__name', 'medicine__name']
    readonly_fields = ['observation']
    fieldsets = (
        ("Week & Center Info", {
            "fields": ("center", "medicine", "week_start", "week_end")
        }),
        ("Consumption", {
            "fields": ("quantity_used",)
        }),
        ("Observation", {
            "fields": ("observation",),
            "classes": ("collapse",)
        }),
    )
