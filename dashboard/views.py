from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from loans.models import LoanApplication
from susu.models import SusuApplication, SusuTransaction, SusuPayoutRequest
from activitylog.models import ActivityLog


# -----------------------------
# HOME
# -----------------------------
def home(request):
    return render(request, 'dashboard/home.html')


# -----------------------------
# CUSTOMER DASHBOARD
# -----------------------------
@login_required
def customer_dashboard(request):
    if request.user.role != 'customer':
        return redirect('/')

    total_loans = LoanApplication.objects.filter(
        customer__email=request.user.email
    ).count()

    total_susu = SusuApplication.objects.filter(
        customer__email=request.user.email
    ).count()

    context = {
        'total_loans': total_loans,
        'total_susu': total_susu,
    }

    return render(request, 'dashboard/customer_dashboard.html', context)


# -----------------------------
# ADMIN DASHBOARD
# -----------------------------
@login_required
def admin_dashboard(request):
    if request.user.role != 'admin':
        return redirect('/')

    context = build_dashboard_context('Admin Dashboard')
    return render(request, 'dashboard/admin_dashboard.html', context)


# -----------------------------
# MANAGEMENT DASHBOARD
# -----------------------------
@login_required
def management_dashboard(request):
    if request.user.role != 'management':
        return redirect('/')

    context = build_dashboard_context('Management Dashboard')
    return render(request, 'dashboard/management_dashboard.html', context)


# -----------------------------
# OPERATOR DASHBOARD
# -----------------------------
@login_required
def operator_dashboard(request):
    if request.user.role != 'operator':
        return redirect('/')

    total_loans = LoanApplication.objects.count()
    pending_loans = LoanApplication.objects.filter(status='pending').count()

    total_susu = SusuApplication.objects.count()
    active_susu = SusuApplication.objects.filter(status='active').count()

    total_transactions = SusuTransaction.objects.count()

    mobile_money_count = ActivityLog.objects.filter(
        action='mobile_money_transaction'
    ).count()

    orange_money_count = ActivityLog.objects.filter(
        action='orange_money_transaction'
    ).count()

    lec_payment_count = ActivityLog.objects.filter(
        action='lec_bill_payment'
    ).count()

    telecom_service_count = ActivityLog.objects.filter(
        action='telecom_service'
    ).count()

    my_daily_activities = ActivityLog.objects.filter(
        user=request.user
    ).order_by('-created_at')[:10]

    context = {
        'dashboard_title': 'Operator Dashboard',
        'total_loans': total_loans,
        'pending_loans': pending_loans,
        'total_susu': total_susu,
        'active_susu': active_susu,
        'total_transactions': total_transactions,
        'mobile_money_count': mobile_money_count,
        'orange_money_count': orange_money_count,
        'lec_payment_count': lec_payment_count,
        'telecom_service_count': telecom_service_count,
        'my_daily_activities': my_daily_activities,
    }

    return render(request, 'dashboard/operator_dashboard.html', context)


# -----------------------------
# SHARED CONTEXT ADMIN + MANAGEMENT
# -----------------------------
def build_dashboard_context(title):
    total_loans = LoanApplication.objects.count()
    approved_loans = LoanApplication.objects.filter(status='approved').count()
    pending_loans = LoanApplication.objects.filter(status='pending').count()
    rejected_loans = LoanApplication.objects.filter(status='rejected').count()

    total_susu = SusuApplication.objects.count()
    active_susu = SusuApplication.objects.filter(status='active').count()
    pending_susu = SusuApplication.objects.filter(status='pending').count()
    rejected_susu = SusuApplication.objects.filter(status='rejected').count()

    total_transactions = SusuTransaction.objects.count()
    total_activities = ActivityLog.objects.count()

    mobile_money_count = ActivityLog.objects.filter(
        action='mobile_money_transaction'
    ).count()

    orange_money_count = ActivityLog.objects.filter(
        action='orange_money_transaction'
    ).count()

    lec_payment_count = ActivityLog.objects.filter(
        action='lec_bill_payment'
    ).count()

    telecom_service_count = ActivityLog.objects.filter(
        action='telecom_service'
    ).count()

    recent_activities = ActivityLog.objects.order_by('-created_at')[:10]
    recent_payout_requests = SusuPayoutRequest.objects.order_by('-created_at')[:10]

    return {
        'dashboard_title': title,
        'total_loans': total_loans,
        'approved_loans': approved_loans,
        'pending_loans': pending_loans,
        'rejected_loans': rejected_loans,
        'total_susu': total_susu,
        'active_susu': active_susu,
        'pending_susu': pending_susu,
        'rejected_susu': rejected_susu,
        'total_transactions': total_transactions,
        'total_activities': total_activities,
        'mobile_money_count': mobile_money_count,
        'orange_money_count': orange_money_count,
        'lec_payment_count': lec_payment_count,
        'telecom_service_count': telecom_service_count,
        'recent_activities': recent_activities,
        'recent_payout_requests': recent_payout_requests,
    }


def about_page(request):
    return render(request, "dashboard/about.html")


def services_page(request):
    return render(request, "dashboard/services.html")


def blog_page(request):
    return render(request, "dashboard/blog.html")