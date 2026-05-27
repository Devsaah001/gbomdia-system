from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("GBOMDIA Account Info", {
            "fields": (
                "role",
                "phone",
                "email_verified",
                "verification_code",
                "reset_code",
            )
        }),
    )

    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "role",
        "phone",
        "email_verified",
        "is_staff",
        "is_active",
    )
    
    search_fields = ("username", "email", "first_name", "last_name", "phone")
    list_filter = ("role", "email_verified", "is_staff", "is_active")