from django.urls import path
from catalog.apps import CatalogConfig
from .views import ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView, ProductDeleteView, \
    ContactView

# Создаем пространство имен с названием catalog/ для страниц contacts.html и products.html и остальных, не забыть
# включить в путь в директории config/urls.py. Для этого используем класс CatalogConfig для вызова имени директории
# в catalog.apps
app_name = CatalogConfig.name

# Создаем маршрутизацию пути html страниц и контроллеров
urlpatterns = [
    path('products/', ProductListView.as_view(), name='products_list'),
    path('contacts/', ContactView.as_view(), name='contacts'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('product/create/', ProductCreateView.as_view(), name='product_create'),
    path('product/update/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),
    path('product/delete/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),
]
