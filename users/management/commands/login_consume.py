from django.core.management import BaseCommand
from users.consumer import login_consume


class Command(BaseCommand):
    def handle(self, *args, **options):
        login_consume()
