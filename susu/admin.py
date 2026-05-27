from django.contrib import admin

from .models import SusuApplication, SusuPayoutRequest, SusuTransaction


@admin.register(SusuApplication)
class SusuApplicationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "customer",
        "account_number",
        "plan_name",
        "contribution_amount",
        "balance",
        "status",
        "created_at",
    )

    search_fields = (
        "customer__first_name",
        "customer__last_name",
        "customer__phone",
        "customer__email",
        "account_number",
    )

    list_filter = ("status", "created_at")


@admin.register(SusuTransaction)
class SusuTransactionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "susu_account",
        "transaction_type",
        "amount",
        "reference",
        "recorded_by",
        "created_at",
    )

    list_filter = ("transaction_type", "created_at")


@admin.register(SusuPayoutRequest)
class SusuPayoutRequestAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "susu_account",
        "requested_amount",
        "status",
        "requested_by",
        "approved_by",
        "created_at",
    )

    list_filter = ("status", "created_at")