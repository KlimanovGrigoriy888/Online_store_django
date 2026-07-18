from django.urls import path
from users.apps import UsersConfig
from django.contrib.auth.views import LoginView, LogoutView

from users.views import RegisterView, email_verification

# Создаем пространство имен с названием users/ для страниц register.html и остальных, не забыть
# включить в путь в директории config/urls.py. Для этого используем класс CatalogConfig для вызова имени директории
# в users.apps
app_name = UsersConfig.name

# Создаем маршрутизацию пути html страниц и контроллеров
# next_page в LoginView.as_view можно заменить на LOGIN_REDIRECT_URL = "catalog:products_list" в settings.py
# next_page в  LogoutView.as_view можно заменить на LOGOUT_REDIRECT_URL = "catalog:products_list" в settings.py
urlpatterns = [
    path('login/', LoginView.as_view(template_name="users/login.html", next_page="catalog:products_list"),
         name='login'),
    path('logout/', LogoutView.as_view(next_page="catalog:products_list"), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path("email-confirm/<str:token>/", email_verification, name='email-confirm'),
]
