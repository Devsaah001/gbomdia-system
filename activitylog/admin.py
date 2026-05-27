from django.contrib import admin

from .models import ActivityLog


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = (
        "action",
        "service_type",
        "status",
        "customer_name",
        "customer_phone",
        "amount",
        "user",
        "created_at",
    )

    search_fields = ("customer_name", "customer_phone", "reference", "note")
    list_filter = ("action", "service_type", "status", "created_at")