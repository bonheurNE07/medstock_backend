from django.db import models
from django.db.models import Sum
from .models import WeeklyConsumptionReport, Stock, MedicineReceipt, MedicineBatch
from datetime import timedelta
from django.utils import timezone

def get_total_consumed_per_center():
    return WeeklyConsumptionReport.objects.values(
        'center__id', 'center__name'
    ).annotate(
        total_consumed=Sum('quantity')
    )

def get_total_stock_per_center():
    return Stock.objects.values(
        'center__id', 'center__name'
    ).annotate(
        total_stock=Sum('quantity')
    )

def get_low_stock_alerts(threshold=10):
    return Stock.objects.filter(quantity__lt=threshold)

def get_top_medicines(limit=5):
    return WeeklyConsumptionReport.objects.values(
        'medicine__id', 'medicine__name'
    ).annotate(
        total_consumed=Sum('quantity')
    ).order_by('-total_consumed')[:limit]

def get_recent_receipts(limit=5):
    return MedicineReceipt.objects.select_related('center', 'medicine').order_by('-date_received')[:limit]

def consume_medicine(center, medicine, quantity):
    total_available = MedicineBatch.objects.filter(
        center=center, medicine=medicine
    ).aggregate(total=models.Sum("quantity"))["total"] or 0

    if quantity > total_available:
        raise ValueError(f"Not enough stock to consume {quantity} units of {medicine}")
    batches = MedicineBatch.objects.filter(center=center, medicine=medicine).order_by("exp_date")
    remaining = quantity
    for batch in batches:
        if batch.quantity >= remaining:
            batch.quantity -= remaining
            batch.save()
            break
        else:
            remaining -= batch.quantity
            batch.quantity = 0
            batch.save()