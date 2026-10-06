import random
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from leads.models import Lead, LeadActivity

User = get_user_model()

FIRST_NAMES = [
    "Alice",
    "Bob",
    "Carol",
    "David",
    "Emma",
    "Frank",
    "Grace",
    "Henry",
    "Ivy",
    "Jack",
    "Kara",
    "Liam",
    "Mia",
    "Noah",
    "Olivia",
    "Peter",
    "Quinn",
    "Ruby",
    "Sam",
    "Tina",
    "Uma",
    "Victor",
    "Wendy",
    "Xander",
]

LAST_NAMES = [
    "Smith",
    "Johnson",
    "Williams",
    "Brown",
    "Jones",
    "Garcia",
    "Miller",
    "Davis",
    "Rodriguez",
    "Martinez",
    "Hernandez",
    "Lopez",
    "Gonzalez",
    "Wilson",
    "Anderson",
    "Thomas",
    "Taylor",
    "Moore",
    "Jackson",
    "Martin",
]

NOTES = [
    "Interested in the premium plan.",
    "Asked for a callback next week.",
    "Wants a demo of the dashboard.",
    "Referred by an existing customer.",
    "Downloaded the pricing PDF.",
    "Requested a quote for 50 seats.",
    "Cold lead — not ready to buy yet.",
    "Very responsive on WhatsApp.",
    "",
    "",
]

ACTIONS = [
    "created",
    "called",
    "emailed",
    "status_changed",
    "note_added",
    "assigned",
]

DESCRIPTIONS = {
    "created": "Lead was created from {source}.",
    "called": "Called the lead, discussed requirements.",
    "emailed": "Sent intro email with product brochure.",
    "status_changed": "Status updated to {status}.",
    "note_added": "Added a note to the lead.",
    "assigned": "Lead assigned to a sales rep.",
}


class Command(BaseCommand):
    help = "Seed the database with sample leads and activities."

    def add_arguments(self, parser):
        parser.add_argument(
            "--count",
            type=int,
            default=50,
            help="Number of leads to create (default: 50).",
        )
        parser.add_argument(
            "--activities",
            type=int,
            default=3,
            help="Max activities per lead (default: 3).",
        )
        parser.add_argument(
            "--flush",
            action="store_true",
            help="Delete all existing leads and activities before seeding.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        count = options["count"]
        max_activities = options["activities"]

        if options["flush"]:
            deleted_activities, _ = LeadActivity.objects.all().delete()
            deleted_leads, _ = Lead.objects.all().delete()
            self.stdout.write(
                self.style.WARNING(
                    f"Flushed {deleted_leads} leads and {deleted_activities} activities."
                )
            )

        users = list(User.objects.all())
        if not users:
            self.stdout.write(
                self.style.WARNING(
                    "No users found — leads will be created without an assignee."
                )
            )

        statuses = [s[0] for s in Lead.Status.choices]
        sources = [s[0] for s in Lead.Source.choices]

        leads_created = 0
        activities_created = 0

        for _ in range(count):
            first = random.choice(FIRST_NAMES)
            last = random.choice(LAST_NAMES)
            name = f"{first} {last}"

            lead = Lead.objects.create(
                name=name,
                phone=f"+1{random.randint(2000000000, 9999999999)}",
                email=f"{first.lower()}.{last.lower()}@example.com",
                source=random.choice(sources),
                note=random.choice(NOTES),
                status=random.choice(statuses),
                assigned_to=random.choice(users)
                if users and random.random() > 0.3
                else None,
            )
            leads_created += 1

            # Backdate created_at a bit so ordering looks natural
            backdate = timezone.now() - timedelta(
                days=random.randint(0, 60),
                hours=random.randint(0, 23),
            )
            Lead.objects.filter(pk=lead.pk).update(created_at=backdate)
            lead.refresh_from_db()

            # Create activities
            num_activities = random.randint(0, max_activities)
            for _ in range(num_activities):
                action = random.choice(ACTIONS)
                description = DESCRIPTIONS[action].format(
                    source=lead.get_source_display(),  # type: ignore
                    status=lead.get_status_display(),  # type: ignore
                )
                LeadActivity.objects.create(
                    lead=lead,
                    user=random.choice(users) if users else None,
                    action=action,
                    description=description,
                )
                activities_created += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Seeded {leads_created} leads and {activities_created} activities."
            )
        )
