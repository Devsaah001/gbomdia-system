from decimal import Decimal

from django.conf import settings
from django.db import models

from customers.models import Customer


class SusuApplication(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("active", "Active"),
        ("closed", "Closed"),
        ("rejected", "Rejected"),
    ]

    MARITAL_STATUS_CHOICES = [
        ("single", "Single"),
        ("married", "Married"),
        ("divorced", "Divorced"),
        ("widowed", "Widowed"),
        ("other", "Other"),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="susu_accounts")
    account_number = models.CharField(max_length=50, unique=True, blank=True, null=True)
    plan_name = models.CharField(max_length=100, default="Standard Susu Plan")
    contribution_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    admin_note = models.TextField(blank=True, null=True)

    marital_status = models.CharField(
        max_length=20,
        choices=MARITAL_STATUS_CHOICES,
        blank=True,
        null=True,
    )
    spouse_name = models.CharField(max_length=200, blank=True, null=True)
    number_of_children = models.PositiveIntegerField(blank=True, null=True)
    household_address = models.TextField(blank=True, null=True)

    next_of_kin_name = models.CharField(max_length=200, blank=True, null=True)
    next_of_kin_phone = models.CharField(max_length=30, blank=True, null=True)
    next_of_kin_relationship = models.CharField(max_length=100, blank=True, null=True)
    next_of_kin_address = models.TextField(blank=True, null=True)

    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="approved_susu_accounts",
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_susu_accounts",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approved_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Susu #{self.id} - {self.customer} - {self.status}"


class SusuTransaction(models.Model):
    TRANSACTION_TYPES = [
        ("deposit", "Deposit"),
        ("withdrawal", "Withdrawal"),
        ("payout", "Payout"),
    ]

    susu_account = models.ForeignKey(SusuApplication, on_delete=models.CASCADE, related_name="transactions")
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    reference = models.CharField(max_length=100, blank=True, null=True)
    note = models.TextField(blank=True, null=True)

    recorded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="recorded_susu_transactions",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        is_new = self.pk is None

        super().save(*args, **kwargs)

        if is_new:
            if self.transaction_type == "deposit":
                self.susu_account.balance += self.amount
            elif self.transaction_type in ["withdrawal", "payout"]:
                self.susu_account.balance -= self.amount

            self.susu_account.save()

    def __str__(self):
        return f"{self.transaction_type} - {self.amount} - {self.susu_account.customer}"


class SusuPayoutRequest(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
        ("paid", "Paid"),
    ]

    susu_account = models.ForeignKey(SusuApplication, on_delete=models.CASCADE, related_name="payout_requests")
    requested_amount = models.DecimalField(max_digits=12, decimal_places=2)
    reason = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    requested_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="requested_susu_payouts",
    )

    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="approved_susu_payouts",
    )

    approved_at = models.DateTimeField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payout Request #{self.id} - {self.susu_account.customer} - {self.status}"