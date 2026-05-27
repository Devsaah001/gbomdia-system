from django.urls import path

from .views import notifications_home


urlpatterns = [
    path("", notifications_home, name="notifications_home"),
]