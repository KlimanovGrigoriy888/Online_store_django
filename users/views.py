import secrets

from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView
from django.contrib.auth import login

from users.forms import UserRegisterForm
from users.models import CustomUser
from config.settings import EMAIL_HOST_USER



# Представление для регистрации пользователя
class RegisterView(CreateView):
    model = CustomUser
    template_name = 'users/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('catalog:products_list')

    def form_valid(self, form):
        user = form.save()  # Django берет данные из формы и создает пользователя в базе
        user.is_active = False  # Делаем пользователя не активным

        # Генерируем и сохраняем токен
        token = secrets.token_hex(16)  # Генерация токена с помощью импорта secrets
        user.token = token  # Записываем этот токен в созданного пользователя
        user.save()  #  Обновляем его в базе данных.

        # Собираем ссылку
        host = self.request.get_host()  # Django узнает текущий адрес сайта (например, 127.0.0.1:8000)
        url = f'http://{host}/users/email-confirm/{token}/' # Формируется ссылка вида http://127.0.0 и отправляется
        # на почту
        send_mail(
            subject="Подтверждение почты",
            message=f"Привет, перейди по ссылке для подтверждения почты {url}",
            from_email=EMAIL_HOST_USER,  # Импорт из settings.py
            recipient_list=[user.email],  # Email полученный от пользователя
            fail_silently=False,
        )
        return super().form_valid(form)

# Отдельная функция для отправки приветственного письма
def send_welcome_email(user_email):
    subject = 'Добро пожаловать в наш сервис'
    message = 'Спасибо, что зарегистрировались в нашем сервисе!'
    from_email = EMAIL_HOST_USER
    recipient_list = [user_email]
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)

def email_verification(request, token):
    user = get_object_or_404(CustomUser, token=token)
    user.is_active = True
    user.token = None  # Стираем токен после использования, чтобы ссылку нельзя было использовать повторно
    user.save()

    #  ОТПРАВКА ПИСЬМА: вызываем функцию и передаем email активированного пользователя
    send_welcome_email(user.email)

    return redirect(reverse("users:login"))  # Импортируем reverse для генерации пути URL