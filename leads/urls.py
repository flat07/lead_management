# leads/urls.py

from django.urls import path

from .views import (
    dashboard,
    lead_create,
    lead_delete,
    lead_detail,
    lead_edit,
    lead_list,
)

urlpatterns = [
    path(
        "",
        dashboard,
        name="dashboard",
    ),
    path(
        "dashboard/",
        dashboard,
        name="dashboard",
    ),
    path(
        "leads/",
        lead_list,
        name="lead-list",
    ),
    path(
        "leads/create/",
        lead_create,
        name="lead-create",
    ),
    path(
        "leads/<int:pk>/",
        lead_detail,
        name="lead-detail",
    ),
    path(
        "leads/<int:pk>/edit/",
        lead_edit,
        name="lead-edit",
    ),
    path(
        "leads/<int:pk>/delete/",
        lead_delete,
        name="lead-delete",
    ),
]
