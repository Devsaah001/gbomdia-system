from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from customers.models import Customer

from .forms import LoanApplicationForm
from .models import LoanApplication


@login_required
def apply_loan(request):
    initial_data = {}

    if request.user.role == "customer":
        initial_data = {
            "first_name": request.user.first_name,
            "last_name": request.user.last_name,
            "phone": request.user.phone,
            "email": request.user.email,
            "interest_rate": "15.00",
        }

    if request.method == "POST":
        form = LoanApplicationForm(request.POST, request.FILES)

        if form.is_valid():
            agree_terms = request.POST.get("agree_terms")

            if not agree_terms:
                messages.error(request, "You must agree to the loan terms and conditions.")
                return render(request, "loans/loan_application.html", {"form": form})

            customer, created = Customer.objects.get_or_create(
                phone=form.cleaned_data["phone"],
                defaults={
                    "first_name": form.cleaned_data["first_name"],
                    "last_name": form.cleaned_data.get("last_name", ""),
                    "email": form.cleaned_data.get("email", ""),
                    "address": form.cleaned_data.get("address", ""),
                    "is_active": True,
                },
            )

            if not created:
                customer.first_name = form.cleaned_data["first_name"]
                customer.last_name = form.cleaned_data.get("last_name", "")
                customer.email = form.cleaned_data.get("email", "")
                customer.address = form.cleaned_data.get("address", "")
                customer.save()

            loan = form.save(commit=False)
            loan.customer = customer
            loan.created_by = request.user
            loan.status = "pending"
            loan.interest_rate = 15
            loan.save()

            messages.success(request, "Loan application submitted successfully.")
            return redirect("my_loans" if request.user.role == "customer" else "manage_loans")

    else:
        form = LoanApplicationForm(initial=initial_data)

    return render(request, "loans/loan_application.html", {"form": form})


@login_required
def my_loans(request):
    loans = LoanApplication.objects.filter(
        customer__email=request.user.email
    ).order_by("-created_at")

    return render(request, "loans/my_loans.html", {"loans": loans})


@login_required
def manage_loans(request):
    if request.user.role not in ["admin", "management", "operator"]:
        return redirect("customer_dashboard")

    loans = LoanApplication.objects.all().order_by("-created_at")
    return render(request, "loans/manage_loans.html", {"loans": loans})


@login_required
def loan_detail(request, loan_id):
    loan = get_object_or_404(LoanApplication, id=loan_id)

    if request.user.role == "customer" and loan.customer.email != request.user.email:
        return redirect("customer_dashboard")

    return render(request, "loans/loan_detail.html", {"loan": loan})


@login_required
def approve_loan(request, loan_id):
    if request.user.role not in ["admin", "management"]:
        messages.error(request, "You do not have permission to approve loans.")
        return redirect("manage_loans")

    loan = get_object_or_404(LoanApplication, id=loan_id)

    if loan.status == "pending":
        loan.status = "approved"
        loan.approved_by = request.user
        loan.approved_at = timezone.now()
        loan.save()
        messages.success(request, "Loan approved successfully.")

    return redirect("manage_loans")


@login_required
def reject_loan(request, loan_id):
    if request.user.role not in ["admin", "management"]:
        messages.error(request, "You do not have permission to reject loans.")
        return redirect("manage_loans")

    loan = get_object_or_404(LoanApplication, id=loan_id)

    if loan.status == "pending":
        loan.status = "rejected"
        loan.approved_by = request.user
        loan.approved_at = timezone.now()
        loan.save()
        messages.success(request, "Loan rejected successfully.")

    return redirect("manage_loans")