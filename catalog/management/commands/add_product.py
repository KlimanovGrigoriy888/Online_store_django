from django.core.management.base import BaseCommand
from catalog.models import Product, Category


class Command(BaseCommand):
    help = "Add test product to the database"

    def handle(self, *args, **kwargs):
        # Удаляем существующие записи
        Product.objects.all().delete()
        Category.objects.all().delete()

        category, _ = Category.objects.get_or_create(name='Ноутбуки',
                                                     description='Ноутбуки, удобные и носимые портативные устройства с функциями настольного компьютера для удобства жизни"')

        products = [
            {'name': 'Lenovo Thinkpad X220',
             'description': '12.7 inch Laptop i5 Gen3nd RAM 8+320G SSD Игровой ноутбук 14", Intel Core i5-2300, RAM 8 ГБ, SSD 320 ГБ, Intel HD Graphics, Windows Home, (001), черный матовый, Русская раскладка',
             'purchase_price': 8000, 'category': category},
            {'name': 'Dell Latitude 5550',
             'description': '15.6", Intel Core i7-1355U, RAM 16 ГБ, SSD 512 ГБ, Intel Iris Xe Graphics, Linux, (5550-7655), серый, Русская раскладка',
             'purchase_price': 110000, 'category': category},
            {'name': 'ASUS TUF Gaming A18',
             'description': 'Игровой ноутбук 18", AMD Ryzen 7 260, RAM 16 ГБ, SSD 512 ГБ, NVIDIA GeForce RTX 5050 для ноутбуков (8 Гб), Без системы, (90NR0NM1-M003D0), серый, Русская раскладка',
             'purchase_price': 110000, 'category': category},
        ]

        for product_data in products:
            product, created = Product.objects.get_or_create(**product_data)
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully added student: {product.name}, {product.created_at}, {product.description}'))
            else:
                self.stdout.write(
                    self.style.WARNING(f'Student already exists: {product.name} {product.description}'))
