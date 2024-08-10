# delete_expired_records.py

from django.core.management.base import BaseCommand
from django.utils import timezone
from webapp.models import Allocated  # Replace 'yourapp' with the name of your Django app


class Command(BaseCommand):
    help = 'Deletes expired records from the Allocated model'

    def handle(self, *args, **options):
        # Get the current date
        current_date = timezone.now().date()

        # Delete records where the date is before today's date
        deleted_count, _ = Allocated.objects.filter(date__lt=current_date).delete()

        self.stdout.write(self.style.SUCCESS(f'Deleted {deleted_count} expired records'))
