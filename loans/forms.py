from django import forms

from .models import LoanApplication


class LoanApplicationForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100, required=False)
    phone = forms.CharField(max_length=30)
    email = forms.EmailField(required=False)

    class Meta:
        model = LoanApplication
        fields = [
            "first_name",
            "last_name",
            "phone",
            "email",

            "address",
            "occupation",
            "employment_status",
            "employer_or_business_name",
            "monthly_income",
            "id_type",
            "id_number",
            "applicant_photo",
            "id_document_photo",
            "collateral_document",
            "collateral_description",

            "amount_requested",
            "duration_months",
            "interest_rate",
            "purpose",

            "guarantor1_full_name",
            "guarantor1_phone",
            "guarantor1_occupation",
            "guarantor1_relationship",
            "guarantor1_address",

            "guarantor2_full_name",
            "guarantor2_phone",
            "guarantor2_occupation",
            "guarantor2_relationship",
            "guarantor2_address",
        ]

        widgets = {
            "purpose": forms.Textarea(attrs={"rows": 4}),
            "address": forms.Textarea(attrs={"rows": 3}),
            "collateral_description": forms.Textarea(attrs={"rows": 3}),
            "guarantor1_address": forms.Textarea(attrs={"rows": 3}),
            "guarantor2_address": forms.Textarea(attrs={"rows": 3}),
            "interest_rate": forms.NumberInput(attrs={"readonly": "readonly"}),
        }