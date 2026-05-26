from django.shortcuts import render
from django.http import HttpResponse
from .models import Product


# Контроллер GET запроса и рендеринга страницы home.html
def view_home(request):
    latest_products = Product.objects.order_by('-created_at')[:5]
    for product in latest_products:
        print(product.name)
    return render(request, 'catalog/home.html')


# Контроллер POST запроса получения обратной связи со страницы и рендеринга страницы contact.html
# И контроллер GET запроса и рендеринга страницы contact.html если не POST запрос
def contact(request):
    if request.method == 'POST':
        # Если метод запроса сервера POST получаем данные с web страницы
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        # Возвращаем простой ответ
        print(f"Спасибо, {name}! Ваше телефон {phone} и сообщение {message} получены.")
        return HttpResponse(f"Спасибо, {name}! Ваше телефон {phone} и сообщение {message} получены.")
    return render(request, 'catalog/contacts.html')
