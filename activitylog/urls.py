from django.urls import path

from .views import my_activities, record_service


urlpatterns = [
    path("services/", record_service, name="record_service"),
    path("my-activities/", my_activities, name="my_activities"),
]