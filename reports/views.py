from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def reports_home(request):
    return render(request, "reports/reports_home.html")