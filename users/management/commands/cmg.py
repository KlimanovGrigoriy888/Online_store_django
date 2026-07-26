from django.core.management import BaseCommand

from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):
    """Команда для создания группы 'Модератор продуктов' с правами изменения статуса публикации и удаления продукта"""
    def handle(self, *args, **options):
        product_moderator = Group.objects.create(name='product_moderator')
        can_unpublish_product = Permission.objects.get(codename='can_unpublish_product')
        can_delete_product = Permission.objects.get(codename='delete_product')
        product_moderator.permissions.add(can_unpublish_product, can_delete_product)
        product_moderator.save()
