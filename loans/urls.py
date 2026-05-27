from django.urls import path

from .views import (
    apply_loan,
    approve_loan,
    loan_detail,
    manage_loans,
    my_loans,
    reject_loan,
)


urlpatterns = [
    path("apply/", apply_loan, name="apply_loan"),
    path("office/apply/", apply_loan, name="office_apply_loan"),
    path("my-loans/", my_loans, name="my_loans"),
    path("admin/manage/", manage_loans, name="manage_loans"),
    path("<int:loan_id>/", loan_detail, name="loan_detail"),
    path("approve/<int:loan_id>/", approve_loan, name="approve_loan"),
    path("reject/<int:loan_id>/", reject_loan, name="reject_loan"),
]