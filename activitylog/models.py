from decimal import Decimal

from django.conf import settings
from django.db import models


class ActivityLog(models.Model):
    ACTION_CHOICES = [
        ("mobile_money_transaction", "Mobile Money Transaction"),
        ("orange_money_transaction", "Orange Money Transaction"),
        ("lec_bill_payment", "LEC Bill Payment"),
        ("telecom_service", "Telecom Service"),
        ("loan_action", "Loan Action"),
        ("susu_action", "Susu Action"),
        ("payout_action", "Payout Action"),
        ("customer_support", "Customer Support"),
        ("other", "Other"),
    ]

    SERVICE_TYPE_CHOICES = [
        ("mtn_mobile_money", "MTN Mobile Money"),
        ("orange_money", "Orange Money"),
        ("lec_purchase", "LEC Purchase"),
        ("loan", "Loan"),
        ("digital_susu", "Digital Susu"),
        ("sim_registration", "SIM Registration"),
        ("forex_exchange", "Forex Exchange"),
        ("other", "Other"),
    ]

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("successful", "Successful"),
        ("failed", "Failed"),
        ("cancelled", "Cancelled"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="activity_logs",
    )

    action = models.CharField(max_length=50, choices=ACTION_CHOICES, default="other")
    service_type = models.CharField(max_length=50, choices=SERVICE_TYPE_CHOICES, default="other")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    customer_name = models.CharField(max_length=200, blank=True, null=True)
    customer_phone = models.CharField(max_length=30, blank=True, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    reference = models.CharField(max_length=100, blank=True, null=True)
    note = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_action_display()} - {self.customer_name or 'N/A'}"