from django.core.management.base import BaseCommand
from website.views import check_and_notify_test_status

class Command(BaseCommand):
    help = 'Checks test statuses and sends notifications if needed'

    def handle(self, *args, **kwargs):
        check_and_notify_test_status()
        self.stdout.write(self.style.SUCCESS('Checked test statuses and sent notifications if needed.'))