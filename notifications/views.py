from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Notification


@login_required
def notifications_home(request):
    notifications = Notification.objects.all().order_by("-created_at")
    return render(
        request,
        "notifications/notifications_home.html",
        {"notifications": notifications},
    )