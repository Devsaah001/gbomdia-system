from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import timezone

from .models import DailyBusinessCash
from activitylog.models import ActivityLog


def role_redirect(user):
    if user.role == "admin":
        return redirect("admin_dashboard")
    if user.role == "management":
        return redirect("management_dashboard")
    if user.role == "operator":
        return redirect("operator_dashboard")
    return redirect("customer_dashboard")


@login_required
def enter_daily_cash(request):
    today = timezone.localdate()

    existing = DailyBusinessCash.objects.filter(
        staff=request.user,
        business_date=today
    ).first()

    if existing:
        return role_redirect(request.user)

    if request.method == "POST":
        opening_amount = Decimal(str(request.POST.get("opening_amount") or "0.00"))

        DailyBusinessCash.objects.create(
            staff=request.user,
            opening_amount=opening_amount,
            business_date=today
        )

        return role_redirect(request.user)

    return render(request, "dailycash/enter_daily_cash.html")


@login_required
def daily_cash_report(request):
    today = timezone.localdate()

    if request.user.role in ["admin", "management"]:
        records = DailyBusinessCash.objects.all().order_by("-business_date", "-created_at")
    else:
        records = DailyBusinessCash.objects.filter(staff=request.user).order_by("-business_date")

    for record in records:
        activities = ActivityLog.objects.filter(
            user=record.staff,
            created_at__date=record.business_date
        )

        total_income = Decimal("0.00")
        total_expense = Decimal("0.00")

        for item in activities:
            amount = Decimal(str(item.amount or "0.00"))

            if item.status in ["completed", "approved", "paid", "success"]:
                total_income += amount

            if item.status in ["expense", "refund", "failed"]:
                total_expense += amount

        record.total_income = total_income
        record.total_expense = total_expense
        record.profit_generated = total_income - total_expense
        record.balance = record.opening_amount + record.profit_generated
        record.save()

    return render(request, "dailycash/daily_cash_report.html", {"records": records})