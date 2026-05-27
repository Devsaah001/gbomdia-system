from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Customer


@login_required
def customer_list(request):
    customers = Customer.objects.all().order_by("-created_at")
    return render(request, "customers/customer_list.html", {"customers": customers})