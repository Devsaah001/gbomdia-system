from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from customers.models import Customer

from .forms import SusuApplicationForm, SusuPayoutRequestForm
from .models import SusuApplication, SusuPayoutRequest


@login_required
def apply_susu(request):
    initial_data = {}

    if request.user.role == "customer":
        initial_data = {
            "first_name": request.user.first_name,
            "last_name": request.user.last_name,
            "phone": request.user.phone,
            "email": request.user.email,
        }

    if request.method == "POST":
        form = SusuApplicationForm(request.POST)

        if form.is_valid():
            customer, created = Customer.objects.get_or_create(
                phone=form.cleaned_data["phone"],
                defaults={
                    "first_name": form.cleaned_data["first_name"],
                    "last_name": form.cleaned_data.get("last_name", ""),
                    "email": form.cleaned_data.get("email", ""),
                    "is_active": True,
                },
            )

            if not created:
                customer.first_name = form.cleaned_data["first_name"]
                customer.last_name = form.cleaned_data.get("last_name", "")
                customer.email = form.cleaned_data.get("email", "")
                customer.save()

            susu = form.save(commit=False)
            susu.customer = customer
            susu.created_by = request.user
            susu.status = "pending"
            susu.save()

            if not susu.account_number:
                susu.account_number = f"GBS-{susu.id:05d}"
                susu.save()

            messages.success(request, "Susu application submitted successfully.")
            return redirect("my_susu" if request.user.role == "customer" else "manage_susu")

    else:
        form = SusuApplicationForm(initial=initial_data)

    return render(request, "susu/susu_application.html", {"form": form})


@login_required
def my_susu(request):
    susu_accounts = SusuApplication.objects.filter(
        customer__email=request.user.email
    ).order_by("-created_at")

    return render(request, "susu/my_susu.html", {"susu_accounts": susu_accounts})


@login_required
def manage_susu(request):
    if request.user.role not in ["admin", "management", "operator"]:
        return redirect("customer_dashboard")

    susu_accounts = SusuApplication.objects.all().order_by("-created_at")
    return render(request, "susu/manage_susu.html", {"susu_accounts": susu_accounts})


@login_required
def approve_susu(request, susu_id):
    if request.user.role not in ["admin", "management"]:
        messages.error(request, "You do not have permission to approve Susu accounts.")
        return redirect("manage_susu")

    susu = get_object_or_404(SusuApplication, id=susu_id)

    if susu.status == "pending":
        susu.status = "active"
        susu.approved_by = request.user
        susu.approved_at = timezone.now()

        if not susu.account_number:
            susu.account_number = f"GBS-{susu.id:05d}"

        susu.save()
        messages.success(request, "Susu account approved successfully.")

    return redirect("manage_susu")


@login_required
def reject_susu(request, susu_id):
    if request.user.role not in ["admin", "management"]:
        messages.error(request, "You do not have permission to reject Susu accounts.")
        return redirect("manage_susu")

    susu = get_object_or_404(SusuApplication, id=susu_id)

    if susu.status == "pending":
        susu.status = "rejected"
        susu.approved_by = request.user
        susu.approved_at = timezone.now()
        susu.save()
        messages.success(request, "Susu account rejected successfully.")

    return redirect("manage_susu")


@login_required
def manage_payout_requests(request):
    if request.user.role not in ["admin", "management", "operator"]:
        return redirect("customer_dashboard")

    payout_requests = SusuPayoutRequest.objects.all().order_by("-created_at")
    return render(
        request,
        "susu/manage_payout_requests.html",
        {"payout_requests": payout_requests},
    )


@login_required
def approve_payout_request(request, payout_id):
    if request.user.role not in ["admin", "management"]:
        messages.error(request, "You do not have permission to approve payout requests.")
        return redirect("manage_payout_requests")

    payout = get_object_or_404(SusuPayoutRequest, id=payout_id)

    if payout.status == "pending":
        payout.status = "approved"
        payout.approved_by = request.user
        payout.approved_at = timezone.now()
        payout.save()
        messages.success(request, "Payout request approved successfully.")

    return redirect("manage_payout_requests")


@login_required
def reject_payout_request(request, payout_id):
    if request.user.role not in ["admin", "management"]:
        messages.error(request, "You do not have permission to reject payout requests.")
        return redirect("manage_payout_requests")

    payout = get_object_or_404(SusuPayoutRequest, id=payout_id)

    if payout.status == "pending":
        payout.status = "rejected"
        payout.approved_by = request.user
        payout.approved_at = timezone.now()
        payout.save()
        messages.success(request, "Payout request rejected successfully.")

    return redirect("manage_payout_requests")