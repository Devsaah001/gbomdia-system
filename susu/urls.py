from django.urls import path

from .views import (
    apply_susu,
    approve_payout_request,
    approve_susu,
    manage_payout_requests,
    manage_susu,
    my_susu,
    reject_payout_request,
    reject_susu,
)


urlpatterns = [
    path("apply/", apply_susu, name="apply_susu"),
    path("office/register/", apply_susu, name="office_register_susu"),
    path("my-susu/", my_susu, name="my_susu"),
    path("admin/manage/", manage_susu, name="manage_susu"),

    path("approve/<int:susu_id>/", approve_susu, name="approve_susu"),
    path("reject/<int:susu_id>/", reject_susu, name="reject_susu"),

    path(
        "payout/manage/",
        manage_payout_requests,
        name="manage_payout_requests"
    ),

    path(
        "payout/approve/<int:payout_id>/",
        approve_payout_request,
        name="approve_payout_request"
    ),

    path(
        "payout/reject/<int:payout_id>/",
        reject_payout_request,
        name="reject_payout_request"
    ),
]