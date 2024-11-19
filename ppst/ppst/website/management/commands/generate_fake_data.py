from django.core.management.base import BaseCommand
from faker import Faker
from website.models import Test, Result, Stimulus_Type, Stimulus, Response, Aggregate, Ticket, Notification
from django.contrib.auth.models import User
from django.utils import timezone
import random

fake = Faker()

class Command(BaseCommand):
    help = 'Generate fake data for testing'

    def handle(self, *args, **kwargs):
        # Generate users if none exist
        if not User.objects.exists():
            for _ in range(5):
                User.objects.create_user(username=fake.user_name(), password="password123")

        users = User.objects.all()

        # Create Stimulus Types
        stimulus_types = ['digit', 'letter', 'mixed']
        for stype in stimulus_types:
            Stimulus_Type.objects.get_or_create(stimulus_type=stype)

        # Generate Stimuli
        for _ in range(10):  # Adjust number as needed
            Stimulus.objects.create(
                stimulus_content=fake.lexify(text="?? ??"),
                stimulus_type=Stimulus_Type.objects.order_by('?').first()
            )

        # Generate Tests
        for _ in range(10):
            test = Test.objects.create(
                user=random.choice(users),
                link=fake.lexify(text="??????"),
                created_at=timezone.now(),
                started_at=timezone.now() - timezone.timedelta(minutes=random.randint(1, 60)),
                finished_at=timezone.now(),
                age=random.randint(20, 80),
                status=random.choice(['pending', 'completed', 'invalid']),
            )

            # Generate Results for each Test
            Result.objects.create(
                test=test,
                character_latencies={str(i): [random.randint(100, 500)] for i in range(5)},
                character_accuracies={str(i): [random.choice([0, 1])] for i in range(5)},
                amount_correct=random.randint(0, 5),
            )

            # Generate Responses for each Test
            for pos in range(5):
                Response.objects.create(
                    response=fake.random_letter(),
                    test=test,
                    time_submitted=timezone.now(),
                    response_position=pos,
                    stimulus=Stimulus.objects.order_by('?').first(),
                )

        # Generate Aggregate Data
        for age_group in [(20, 29), (30, 39), (40, 49)]:
            Aggregate.objects.create(
                min_age=age_group[0],
                max_age=age_group[1],
                average_latencies={f"fourdigit_{i}": random.randint(100, 300) for i in range(3)},
                average_accuracies={f"fourdigit_{i}": round(random.uniform(0.5, 0.9), 2) for i in range(3)},
            )

        # Generate Tickets
        for _ in range(10):
            Ticket.objects.create(
                user=random.choice(users),
                category=random.choice(['general', 'technical', 'account', 'bug/error']),
                description=fake.paragraph(),
                created_at=timezone.now(),
            )

        # Generate Notifications
        for _ in range(10):
            Notification.objects.create(
                user=random.choice(users),
                header=fake.sentence(nb_words=6),
                message=fake.sentence(nb_words=12),
                time_created=timezone.now(),
                is_dismissed=random.choice([True, False]),
            )

        self.stdout.write(self.style.SUCCESS('Successfully generated fake data'))
