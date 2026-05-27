from django.urls import path

from .views import (
    admin_dashboard,
    customer_dashboard,
    management_dashboard,
    operator_dashboard,
)


urlpatterns = [
    path("", customer_dashboard, name="customer_dashboard"),
    path("admin/", admin_dashboard, name="admin_dashboard"),
    path("management/", management_dashboard, name="management_dashboard"),
    path("operator/", operator_dashboard, name="operator_dashboard"),
]