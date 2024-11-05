from django.core.management.base import BaseCommand
from datetime import timedelta
from django.utils import timezone
from website.models import Test, Notification

class Command(BaseCommand):
    help = 'Send notifications for tests that are nearing expiration (6 days old).'

    def handle(self, *args, **kwargs):
        # Find tests that are pending and 6 days old (but not yet expired)
        tests_near_expiry = Test.objects.filter(
            status='pending',
            created_at__lt=timezone.now() - timedelta(days=6),
            created_at__gte=timezone.now() - timedelta(weeks=1)
        )

        for test in tests_near_expiry:
            Notification.objects.create(
                user=test.user,
                test=test,
                header="Test Nearing Expiry",
                message=f"The test with link {test.link} is nearing its expiration (6 days old).",
                time_created=timezone.now()
            )
            self.stdout.write(self.style.SUCCESS(f'Notification sent for test: {test.link}'))

        if not tests_near_expiry:
            self.stdout.write(self.style.WARNING('No tests nearing expiration found.'))
