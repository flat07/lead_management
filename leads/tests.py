# leads/tests.py

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from .models import Lead

User = get_user_model()


class LeadModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="password123",
        )

    def test_create_lead(self):
        lead = Lead.objects.create(
            name="John Smith",
            email="john@example.com",
            source=Lead.Source.WEBSITE,
        )

        self.assertEqual(
            lead.status,
            Lead.Status.NEW,
        )

        self.assertEqual(
            str(lead),
            "John Smith",
        )


class LeadViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="password123",
        )

        self.client.login(
            username="testuser",
            password="password123",
        )

    def test_dashboard_requires_authentication(self):
        self.client.logout()

        response = self.client.get(reverse("dashboard"))

        self.assertEqual(
            response.status_code,
            302,
        )

    def test_create_lead(self):
        response = self.client.post(
            reverse("lead-create"),
            {
                "name": "Jane Doe",
                "email": "jane@example.com",
                "phone": "",
                "source": "website",
                "status": "new",
                "note": "Interested in product",
            },
        )

        self.assertEqual(
            response.status_code,
            302,
        )

        self.assertEqual(
            Lead.objects.count(),
            1,
        )


class LeadAPITests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="apiuser",
            password="password123",
        )

        self.client = APIClient()

        self.client.force_authenticate(user=self.user)

    def test_create_lead_api(self):
        response = self.client.post(
            "/api/leads/",
            {
                "name": "API Lead",
                "email": "api@example.com",
                "source": "website",
                "status": "new",
                "note": "API test",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            201,
        )

        self.assertEqual(
            Lead.objects.count(),
            1,
        )

    def test_list_leads_api(self):
        Lead.objects.create(
            name="Lead One",
            email="one@example.com",
        )

        Lead.objects.create(
            name="Lead Two",
            email="two@example.com",
        )

        response = self.client.get("/api/leads/")

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertEqual(
            response.data["count"],  # type: ignore
            2,
        )

    def test_filter_by_status(self):
        Lead.objects.create(
            name="New Lead",
            email="new@example.com",
            status=Lead.Status.NEW,
        )

        Lead.objects.create(
            name="Won Lead",
            email="won@example.com",
            status=Lead.Status.WON,
        )

        response = self.client.get("/api/leads/?status=won")

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertEqual(
            response.data["count"],  # type: ignore
            1,
        )

    def test_search_leads(self):
        Lead.objects.create(
            name="John Smith",
            email="john@example.com",
        )

        Lead.objects.create(
            name="Jane Doe",
            email="jane@example.com",
        )

        response = self.client.get("/api/leads/?search=John")

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertEqual(
            response.data["count"],  # type: ignore
            1,
        )

    def test_unauthenticated_api(self):
        self.client.force_authenticate(user=None)  # type: ignore

        response = self.client.get("/api/leads/")

        self.assertEqual(
            response.status_code,
            403,
        )
