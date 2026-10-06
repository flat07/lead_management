# leads/serializers.py

from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from rest_framework import serializers

from .models import Lead, LeadActivity


class LeadSerializer(serializers.ModelSerializer):
    assigned_to_name = serializers.CharField(
        source="assigned_to.username",
        read_only=True,
    )

    class Meta:
        model = Lead

        fields = (
            "id",
            "name",
            "phone",
            "email",
            "source",
            "note",
            "status",
            "assigned_to",
            "assigned_to_name",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
            "assigned_to_name",
        )

    def validate(self, attrs):
        phone = attrs.get("phone")
        email = attrs.get("email")

        if not phone and not email:
            raise serializers.ValidationError("Either phone or email is required.")

        return attrs

    def validate_name(self, value):
        value = value.strip()

        if len(value) < 2:
            raise serializers.ValidationError(
                "Name must contain at least 2 characters."
            )

        return value

    def validate_email(self, value):
        if value:
            try:
                validate_email(value)
            except ValidationError:
                raise serializers.ValidationError("Enter a valid email address.")

        return value


class LeadActivitySerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(
        source="user.username",
        read_only=True,
    )

    class Meta:
        model = LeadActivity

        fields = (
            "id",
            "action",
            "description",
            "user",
            "user_name",
            "created_at",
        )

        read_only_fields = (
            "id",
            "user",
            "user_name",
            "created_at",
        )
