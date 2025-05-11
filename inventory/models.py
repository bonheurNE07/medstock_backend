from django.db import models
from django.utils import timezone

class MedicalCenter(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Medicine(models.Model):
    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=20) 

    def __str__(self):
        return f"{self.name} ({self.unit})"

class Stock(models.Model):
    center = models.ForeignKey(MedicalCenter, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['center', 'medicine']

class MedicineReceipt(models.Model):
    center = models.ForeignKey(MedicalCenter, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity_received = models.PositiveIntegerField()
    received_date = models.DateField(default=timezone.now)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update stock
        stock, created = Stock.objects.get_or_create(center=self.center, medicine=self.medicine)
        stock.quantity += self.quantity_received
        stock.save()

class WeeklyConsumptionReport(models.Model):
    week_start = models.DateField()
    week_end = models.DateField()
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    center = models.ForeignKey(MedicalCenter, on_delete=models.CASCADE)
    quantity_used = models.PositiveIntegerField()
    observation = models.TextField(blank=True)

    class Meta:
        unique_together = ['week_start', 'week_end', 'medicine', 'center']
        ordering = ['-week_end']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update stock
        stock = Stock.objects.get(center=self.center, medicine=self.medicine)
        stock.quantity = max(0, stock.quantity - self.quantity_used)
        stock.save()

        # Set observation
        if stock.quantity == 0:
            self.observation = "Rupture de stock"
        elif stock.quantity <= 10:
            self.observation = "Stock faible"
        else:
            self.observation = "Stock suffisant"
        super().save(update_fields=['observation'])
