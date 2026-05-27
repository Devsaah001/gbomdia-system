from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import DailyBusinessCash


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
        opening_amount = request.POST.get("opening_amount")

        DailyBusinessCash.objects.create(
            staff=request.user,
            opening_amount=opening_amount,
            business_date=today
        )

        return role_redirect(request.user)

    return render(request, "dailycash/enter_daily_cash.html")


@login_required
def close_daily_cash(request):
    today = timezone.localdate()

    cash = get_object_or_404(
        DailyBusinessCash,
        staff=request.user,
        business_date=today
    )

    if request.method == "POST":
        cash.closing_amount = Decimal(request.POST.get("closing_amount") or "0")
        cash.total_income = Decimal(request.POST.get("total_income") or "0")
        cash.total_expense = Decimal(request.POST.get("total_expense") or "0")
        cash.save()

        return redirect("daily_cash_report")

    return render(request, "dailycash/close_daily_cash.html", {"cash": cash})


@login_required
def daily_cash_report(request):
    if request.user.role in ["admin", "management"]:
        records = DailyBusinessCash.objects.all().order_by("-business_date", "-created_at")
    else:
        records = DailyBusinessCash.objects.filter(staff=request.user).order_by("-business_date")

    return render(request, "dailycash/daily_cash_report.html", {"records": records})