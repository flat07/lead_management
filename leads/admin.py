# leads/admin.py

from django.contrib import admin

from .models import Lead, LeadActivity


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "email",
        "phone",
        "source",
        "status",
        "assigned_to",
        "created_at",
    )

    list_filter = (
        "status",
        "source",
        "created_at",
    )

    search_fields = (
        "name",
        "email",
        "phone",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )


@admin.register(LeadActivity)
class LeadActivityAdmin(admin.ModelAdmin):
    list_display = (
        "lead",
        "action",
        "user",
        "created_at",
    )

    list_filter = (
        "action",
        "created_at",
    )

    search_fields = (
        "lead__name",
        "description",
    )

    readonly_fields = ("created_at",)
