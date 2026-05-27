from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import InventoryItem


@login_required
def inventory_home(request):
    items = InventoryItem.objects.all().order_by("-created_at")
    return render(request, "inventory/inventory_home.html", {"items": items})