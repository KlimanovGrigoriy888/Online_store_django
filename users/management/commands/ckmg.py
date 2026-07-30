from django.core.management import BaseCommand

from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):
    """Команда для создания группы 'Контент-менеджер' с правами изменения публикациями в блоке"""
    def handle(self, *args, **options):
        content_manager = Group.objects.create(name='content_manager')
        add_blog_permission = Permission.objects.get(codename='add_blog')
        change_blog_permission = Permission.objects.get(codename='change_blog')
        delete_blog_permission = Permission.objects.get(codename='delete_blog')
        content_manager.permissions.add(add_blog_permission, change_blog_permission, delete_blog_permission)
        content_manager.save()
