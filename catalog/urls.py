from django.urls import path
from . import views
from catalog.apps import CatalogConfig

# Создаем пространство имен с названием catalog/ для страниц contacts.html и home.html, не забыть включить в путь в
# директории config/urls.py
app_name = CatalogConfig.name

# Создаем маршрутизацию пути html страниц и контроллеров
urlpatterns = [
    path('home/', views.view_home, name='home'),
    path('contacts/', views.contact, name='contacts')
]
