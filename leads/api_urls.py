# leads/api_urls.py

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .api_views import (
    DashboardAPIView,
    LeadViewSet,
)

router = DefaultRouter()

router.register(
    "leads",
    LeadViewSet,
    basename="lead",
)

urlpatterns = [
    path(
        "",
        include(router.urls),
    ),
    path(
        "dashboard/",
        DashboardAPIView.as_view(),
        name="api-dashboard",
    ),
]
