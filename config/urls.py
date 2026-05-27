from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from dashboard.views import home, about_page, services_page, blog_page


urlpatterns = [
    path("admin/", admin.site.urls),

    path("", home, name="home"),
    path("about/", about_page, name="about_page"),
    path("services/", services_page, name="services_page"),
    path("blog/", blog_page, name="blog_page"),

    path("accounts/", include("accounts.urls")),
    path("dashboard/", include("dashboard.urls")),
    path("customers/", include("customers.urls")),
    path("loans/", include("loans.urls")),
    path("susu/", include("susu.urls")),
    path("activitylog/", include("activitylog.urls")),
    path("inventory/", include("inventory.urls")),
    path("reports/", include("reports.urls")),
    path("notifications/", include("notifications.urls")),
    path("dailycash/", include("dailycash.urls")),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)