from decimal import Decimal
from django.conf import settings
from django.db import models
from django.utils import timezone


class DailyBusinessCash(models.Model):
    staff = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    business_date = models.DateField(default=timezone.localdate)

    opening_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    closing_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))

    total_income = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    total_expense = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    profit_generated = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("staff", "business_date")

    def save(self, *args, **kwargs):

        opening = Decimal(str(self.opening_amount or "0.00"))
        income = Decimal(str(self.total_income or "0.00"))
        expense = Decimal(str(self.total_expense or "0.00"))

        self.profit_generated = income - expense
        self.balance = opening + self.profit_generated

        super().save(*args, **kwargs)