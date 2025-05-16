import uuid
from django.db import models
from django.utils import timezone
from django.db import transaction
from datetime import date

class MedicalCenter(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Medicine(models.Model):
    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name} ({self.unit})"

class MedicineBatch(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    center = models.ForeignKey(MedicalCenter, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    exp_date = models.DateField(blank=True, null=True)
    received_date = models.DateField(default=timezone.now)
    batch_code = models.CharField(max_length=100, blank=True, unique=True)

    @property
    def formatted_exp_date(self):
        return self.exp_date.strftime('%d/%m/%Y') if self.exp_date else ''

    @property
    def formatted_received_date(self):
        return self.received_date.strftime('%d/%m/%Y') if self.received_date else ''

    def save(self, *args, **kwargs):
        if not self.batch_code:
            self.batch_code = f"BATCH-{uuid.uuid4().hex[:8]}"
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['exp_date']
    
    @property
    def is_expired(self):
        return self.exp_date < date.today()

    @property
    def is_depleted(self):
        return self.quantity == 0
    

    def __str__(self):
        return f"{self.medicine.name} - {self.exp_date} - Qty: {self.quantity}"

class Stock(models.Model):
    center = models.ForeignKey(MedicalCenter, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    total_quantity = models.PositiveIntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['center', 'medicine']

class MedicineReceipt(models.Model):
    center = models.ForeignKey(MedicalCenter, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity_received = models.PositiveIntegerField()
    exp_date = models.DateField(blank=True, null=True)
    received_date = models.DateField(default=timezone.now)

    @property
    def formatted_received_date(self):
        return self.received_date.strftime('%d/%m/%Y')

    @property
    def formatted_exp_date(self):
        return self.exp_date.strftime('%d/%m/%Y') if self.exp_date else ''

    def save(self, *args, **kwargs):
        with transaction.atomic():
            super().save(*args, **kwargs)

            # 1. Create a batch
            MedicineBatch.objects.create(
                center=self.center,
                medicine=self.medicine,
                quantity=self.quantity_received,
                exp_date=self.exp_date,
                received_date=self.received_date
            )

            # 2. Update total stock
            total = MedicineBatch.objects.filter(
                center=self.center, medicine=self.medicine
            ).aggregate(total=models.Sum("quantity"))["total"] or 0

            stock, _ = Stock.objects.get_or_create(center=self.center, medicine=self.medicine)
            stock.total_quantity = total
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
    
    @property
    def formatted_week_start(self):
        return self.week_start.strftime('%d/%m/%Y')

    @property
    def formatted_week_end(self):
        return self.week_end.strftime('%d/%m/%Y')

    def save(self, *args, **kwargs):
        with transaction.atomic():
            is_new = self.pk is None
            super().save(*args, **kwargs)

            if is_new:
                # 1. Consume from batches
                consume_medicine(self.center, self.medicine, self.quantity_used)

                # 2. Update stock cache
                total = MedicineBatch.objects.filter(
                    center=self.center, medicine=self.medicine
                ).aggregate(total=models.Sum("quantity"))["total"] or 0

                stock, _ = Stock.objects.get_or_create(center=self.center, medicine=self.medicine)
                stock.total_quantity = total
                stock.save()

                # 3. Update observation
                if total == 0:
                    self.observation = "Rupture de stock"
                elif total <= 10:
                    self.observation = "Stock faible"
                else:
                    self.observation = "Stock suffisant"

                super().save(update_fields=["observation"])


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
