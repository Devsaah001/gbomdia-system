from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import ActivityLogForm
from .models import ActivityLog


@login_required
def record_service(request):
    if request.method == "POST":
        form = ActivityLogForm(request.POST)

        if form.is_valid():
            activity = form.save(commit=False)
            activity.user = request.user
            activity.save()

            messages.success(request, "Service activity recorded successfully.")
            return redirect("my_activities")

    else:
        form = ActivityLogForm()

    return render(request, "activitylog/record_service.html", {"form": form})


@login_required
def my_activities(request):
    activities = ActivityLog.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "activitylog/my_activities.html", {"activities": activities})