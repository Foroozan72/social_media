from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Delete all user accounts except superuser'

    def handle(self, *args, **options):
        # Delete all non-superuser accounts
        User.objects.filter(is_superuser=False).delete()
        self.stdout.write(self.style.SUCCESS('Deleted non-superuser accounts'))
