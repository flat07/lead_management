# leads/api_views.py

from django.db.models import Count
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Lead, LeadActivity
from .serializers import (
    LeadActivitySerializer,
    LeadSerializer,
)


class LeadViewSet(viewsets.ModelViewSet):
    queryset = Lead.objects.select_related("assigned_to").all()

    serializer_class = LeadSerializer
    permission_classes = (IsAuthenticated,)

    filterset_fields = (
        "status",
        "source",
        "assigned_to",
    )

    search_fields = (
        "name",
        "phone",
        "email",
        "note",
    )

    ordering_fields = (
        "name",
        "status",
        "source",
        "created_at",
        "updated_at",
    )

    ordering = ("-created_at",)

    def perform_create(self, serializer):
        lead = serializer.save(assigned_to=self.request.user)

        LeadActivity.objects.create(
            lead=lead,
            user=self.request.user,
            action="created",
            description="Lead created",
        )

    def perform_update(self, serializer):
        old_status = serializer.instance.status

        lead = serializer.save()

        if old_status != lead.status:
            LeadActivity.objects.create(
                lead=lead,
                user=self.request.user,
                action="status_changed",
                description=(f"Status changed from {old_status} to {lead.status}"),
            )

        else:
            LeadActivity.objects.create(
                lead=lead,
                user=self.request.user,
                action="updated",
                description="Lead information updated",
            )

    def perform_destroy(self, instance):
        LeadActivity.objects.create(
            lead=instance,
            user=self.request.user,
            action="deleted",
            description="Lead deleted",
        )

        instance.delete()

    @action(
        detail=True,
        methods=["get"],
        url_path="activities",
    )
    def activities(self, request, pk=None):
        lead = self.get_object()

        activities = lead.activities.select_related("user")

        serializer = LeadActivitySerializer(
            activities,
            many=True,
        )

        return Response(serializer.data)


class DashboardAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        counts = Lead.objects.values("status").annotate(total=Count("id"))

        result = {
            "total": Lead.objects.count(),
            "new": 0,
            "contacted": 0,
            "qualified": 0,
            "won": 0,
            "lost": 0,
        }

        for item in counts:
            result[item["status"]] = item["total"]

        return Response(result)
