from datetime import timedelta
from decimal import Decimal

from django.conf import settings
from django.db import models
from django.utils import timezone

from customers.models import Customer


class LoanApplication(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
        ("disbursed", "Disbursed"),
        ("completed", "Completed"),
        ("overdue", "Overdue"),
    ]

    EMPLOYMENT_CHOICES = [
        ("employed", "Employed"),
        ("self_employed", "Self Employed"),
        ("business_owner", "Business Owner"),
        ("student", "Student"),
        ("unemployed", "Unemployed"),
        ("other", "Other"),
    ]

    ID_TYPE_CHOICES = [
        ("national_id", "National ID"),
        ("voter_id", "Voter ID"),
        ("passport", "Passport"),
        ("drivers_license", "Driver License"),
        ("other", "Other"),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="loans")

    amount_requested = models.DecimalField(max_digits=12, decimal_places=2)
    purpose = models.TextField()
    duration_months = models.PositiveIntegerField(default=1)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal("15.00"))

    address = models.TextField(blank=True, null=True)
    occupation = models.CharField(max_length=150, blank=True, null=True)
    employment_status = models.CharField(
        max_length=30,
        choices=EMPLOYMENT_CHOICES,
        default="other",
        blank=True,
        null=True,
    )
    employer_or_business_name = models.CharField(max_length=200, blank=True, null=True)
    monthly_income = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
        blank=True,
        null=True,
    )

    id_type = models.CharField(
        max_length=30,
        choices=ID_TYPE_CHOICES,
        default="other",
        blank=True,
        null=True,
    )
    id_number = models.CharField(max_length=100, blank=True, null=True)

    guarantor1_full_name = models.CharField(max_length=200, blank=True, null=True)
    guarantor1_phone = models.CharField(max_length=30, blank=True, null=True)
    guarantor1_address = models.TextField(blank=True, null=True)
    guarantor1_occupation = models.CharField(max_length=150, blank=True, null=True)
    guarantor1_relationship = models.CharField(max_length=100, blank=True, null=True)

    guarantor2_full_name = models.CharField(max_length=200, blank=True, null=True)
    guarantor2_phone = models.CharField(max_length=30, blank=True, null=True)
    guarantor2_address = models.TextField(blank=True, null=True)
    guarantor2_occupation = models.CharField(max_length=150, blank=True, null=True)
    guarantor2_relationship = models.CharField(max_length=100, blank=True, null=True)

    applicant_photo = models.ImageField(upload_to="loan_applicants/", blank=True, null=True)
    id_document_photo = models.ImageField(upload_to="loan_ids/", blank=True, null=True)
    collateral_document = models.FileField(upload_to="loan_collateral/", blank=True, null=True)
    collateral_description = models.TextField(blank=True, null=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    admin_note = models.TextField(blank=True, null=True)

    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="approved_loans",
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_loans",
    )

    amount_approved = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    total_repayable = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approved_at = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        monthly_interest_rate = Decimal("0.15")

        if self.amount_requested and self.duration_months:
           self.interest_rate = Decimal("15.00")

           interest_amount = (
               self.amount_requested *
               monthly_interest_rate *
               Decimal(self.duration_months)
           )

           self.total_repayable = self.amount_requested + interest_amount

           if not self.amount_approved or self.amount_approved == Decimal("0.00"):
               self.amount_approved = self.amount_requested

           if not self.balance or self.balance == Decimal("0.00"):
               self.balance = self.total_repayable

        if self.status == "approved":
           self.status = "disbursed"

        if self.status == "disbursed" and self.approved_at and self.duration_months:
           due_date = self.approved_at + timedelta(days=int(self.duration_months) * 30)

           if timezone.now() > due_date and self.balance > 0:
            self.status = "overdue"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Loan #{self.id} - {self.customer} - {self.status}"