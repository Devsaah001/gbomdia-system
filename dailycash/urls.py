from django.urls import path
from .views import enter_daily_cash, close_daily_cash, daily_cash_report

urlpatterns = [
    path("enter/", enter_daily_cash, name="enter_daily_cash"),
    path("close/", close_daily_cash, name="close_daily_cash"),
    path("report/", daily_cash_report, name="daily_cash_report"),
]