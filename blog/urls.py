from django.urls import path
from .apps import BlogConfig
from .views import BlogListView, BlogDetailView, BlogCreateView, BlogUpdateView, BlogDeleteView


# Создаем пространство имен с названием blog/ для страниц contacts.html и products_list.html, не забыть включить в путь
# в директории config/urls.py. Для этого используем класс CatalogConfig для вызова имени директории в catalog.apps
app_name = BlogConfig.name


# Создаем маршрутизацию пути html страниц и контроллеров
urlpatterns = [
    path('', BlogListView.as_view(), name='blog_list'),
    path('create/', BlogCreateView.as_view(), name='blog_create'),

    path('delete/<int:pk>/', BlogDeleteView.as_view(), name='blog_delete'),
    path('update/<int:pk>/', BlogUpdateView.as_view(), name='blog_update'),

    path('view/<int:pk>/', BlogDetailView.as_view(), name='blog_detail'),
]
