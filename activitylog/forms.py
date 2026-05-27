from django import forms

from .models import ActivityLog


class ActivityLogForm(forms.ModelForm):
    class Meta:
        model = ActivityLog
        fields = [
            "action",
            "service_type",
            "status",
            "customer_name",
            "customer_phone",
            "amount",
            "reference",
            "note",
        ]

        widgets = {
            "note": forms.Textarea(attrs={"rows": 4}),
        }