from django import forms

from .models import SusuApplication, SusuPayoutRequest


class SusuApplicationForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100, required=False)
    phone = forms.CharField(max_length=30)
    email = forms.EmailField(required=False)

    class Meta:
        model = SusuApplication
        fields = [
            "first_name",
            "last_name",
            "phone",
            "email",

            "plan_name",
            "contribution_amount",
            "marital_status",
            "spouse_name",
            "number_of_children",
            "household_address",
            "next_of_kin_name",
            "next_of_kin_phone",
            "next_of_kin_relationship",
            "next_of_kin_address",
        ]

        widgets = {
            "household_address": forms.Textarea(attrs={"rows": 3}),
            "next_of_kin_address": forms.Textarea(attrs={"rows": 3}),
        }


class SusuPayoutRequestForm(forms.ModelForm):
    class Meta:
        model = SusuPayoutRequest
        fields = ["requested_amount", "reason"]

        widgets = {
            "reason": forms.Textarea(attrs={"rows": 4}),
        }