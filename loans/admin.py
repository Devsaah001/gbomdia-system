from django.contrib import admin

from .models import LoanApplication


@admin.register(LoanApplication)
class LoanApplicationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "customer",
        "amount_requested",
        "duration_months",
        "interest_rate",
        "total_repayable",
        "balance",
        "status",
        "created_at",
    )

    search_fields = (
        "customer__first_name",
        "customer__last_name",
        "customer__phone",
        "customer__email",
        "purpose",
        "id_number",
    )

    list_filter = ("status", "employment_status", "id_type", "created_at")