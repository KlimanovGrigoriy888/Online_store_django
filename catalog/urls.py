from django.urls import path
from mypy.types import names

from . import views
from catalog.apps import CatalogConfig

# Создаем пространство имен с названием catalog/ для страниц contacts.html и home.html, не забыть включить в путь в
# директории config/urls.py. Для этого используем класс CatalogConfig для вызова имени директории в catalog.apps
app_name = CatalogConfig.name

# Создаем маршрутизацию пути html страниц и контроллеров
urlpatterns = [
    path('home/', views.view_home, name='home'),
    path('contacts/', views.contact, name='contacts'),
    path('product_detail/<int:product_id>/', views.product_detail, name='product_detail'),
    path('product_input', views.product_input_form, name='product_input'),
]
