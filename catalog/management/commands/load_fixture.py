from django.core.management import BaseCommand, call_command
from catalog.models import Product, Category

class Command(BaseCommand):
    help = 'Load test data from fixture'

    def handle(self, *args, **kwargs):
        # # Удаляем существующие записи
        # Product.objects.all().delete()
        # Category.objects.all().delete()

        call_command('loaddata', 'products_fixture.json')
        self.stdout.write(self.style.SUCCESS('Successfully loaded data from fixture'))
