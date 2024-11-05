from django.core.management.base import BaseCommand
from datetime import timedelta
from django.utils import timezone
from models import Test, Notification

class Command(BaseCommand):
    help = 'Check for tests that should be marked as expired.'

    def handle(self, *args, **kwargs):
        expired_tests = Test.objects.filter(
            status='pending',
            created_at__lt=timezone.now() - timedelta(weeks=1)
        )
        for test in expired_tests:
            test.status = 'invalid'
            test.save()
            Notification.objects.create(
                user=test.user,
                test=test,
                header="Test Expired",
                message=f"The test with link {test.link} has expired and is marked as invalid.",
                time_created=timezone.now()
            )
        self.stdout.write(self.style.SUCCESS('Expired tests updated successfully.'))
