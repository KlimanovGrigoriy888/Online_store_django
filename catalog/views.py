from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Product, Category


# Контроллер GET запроса и рендеринга страницы home.html и рендеринга product_detail.html по POST запросу ID продукта
def view_home(request):
    if request.method == 'POST':
        # Получаем product_id из POST-запроса формы
        product_id = request.POST.get('product_id')

        if product_id and product_id.isdigit():
            # Ищем продукт в базе. Если не нашли — выдаст 404. Этот код подсказал ИИ.
            product = get_object_or_404(Product, id=int(product_id))
            # Перенаправляем к контроллеру product_detail товара, передавая искомый product_id
            return redirect('catalog:product_detail', product_id=product.id)

    # Получаем все продукты из класса Product
    products = Product.objects.all()
    context = {'products': products}

    # Получаем все отсортированные по дате создания последние 5 продуктов из класса Product
    latest_products = Product.objects.order_by('-created_at')[:5]
    for product in latest_products:
        print(product.name)
    return render(request, 'catalog/home.html', context)


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


# И контроллер GET запроса и рендеринга страницы product_detail.html с контекстом по id продукта
def product_detail(request, product_id):
    # используем get_object_or_404 вместо падения сервера покажет пользователю стандартную
    # страницу «404: Страница не найдена».
    product = get_object_or_404(Product, id=product_id)
    context = {'product': product}
    return render(request, 'catalog/product_detail.html', context)


def product_input_form(request):
    # если метод POST, то получаем данные с формы product_input.html
    if request.method == 'POST':
        # 1. Получаем текстовые данные из POST
        name = request.POST.get('name')
        purchase_price = request.POST.get('purchase_price')
        description = request.POST.get('description')

        # Получаем ID категории, которую выбрал пользователь в выпадающем списке
        category_id = request.POST.get('category')

        # Находим эту категорию в базе данных
        category = Category.objects.get(id=category_id)

        # 2. Получаем картинку берем из FILES
        picture = request.FILES.get('picture')

        # 3. Создаем и сохраняем новый продукт в базу данных
        new_product = Product.objects.create(
            name=name,
            purchase_price=purchase_price,
            description=description,
            picture=picture,
            category=category  # Передаем объект категории
        )

        # 4. Перенаправляем пользователя на главную страницу каталога чтобы он сразу увидел добавленный товар в списке
        return redirect('catalog:home')

    # Для GET-запроса: забираем ВСЕ категории из базы данных
    categories = Category.objects.all()

    return render(request, 'catalog/product_input.html', {'categories': categories})
