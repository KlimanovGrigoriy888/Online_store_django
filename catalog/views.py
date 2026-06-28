from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import View

from .models import Product
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView, DetailView, DeleteView


class ProductListView(ListView):
    """Класс просмотра всех продуктов."""
    model = Product
    # Новый шаблон страницы для просмотра всех продуктов
    template_name = 'catalog/products_list.html'
    # Контекст передаваемый в шаблон
    context_object_name = 'products'

    def get_queryset(self):
        """Здесь выводим в консоль 5 последних товаров"""
        queryset = super().get_queryset()

        # Получаем все отсортированные по дате создания последние 5 продуктов из класса Product для вывода в консоль
        latest_products = Product.objects.order_by('-created_at')[:5]
        print("--- Последние 5 товаров в БД ---")
        for item in latest_products:
            print(item.name)

        return queryset

    def post(self, request, *args, **kwargs):
        """Этот метод перехватывает POST-запрос от формы ввода ID с базового шаблона. Подсказал ИИ"""

        product_id = request.POST.get('product_id')

        if product_id and product_id.isdigit():
            # Делаем редирект на страницу деталей по запрашиваемому product_id в форме, ищет через адрес и pk через
            # адрес указанный в urls.py адрес 'product/<int:pk>/'
            return redirect('catalog:product_detail', pk=int(product_id))

        return redirect('catalog:products_list')


class ContactView(View):
    """Класс-контроллер для отображения страницы контактов и обработки формы."""

    def get(self, request):
        """Рендеринг страницы контактов при обычном переходе (GET-запрос)."""
        return render(request, 'catalog/contacts.html')

    def post(self, request):
        """Получение данных обратной связи из формы (POST-запрос)."""
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        # Выводим в консоль, как у вас и было изначально
        print(f"Спасибо, {name}! Ваш телефон {phone} и сообщение '{message}' получены.")

        # Возвращаем простой HTTP-ответ на экран
        return HttpResponse(f"Спасибо, {name}! Ваш телефон {phone} и сообщение '{message}' получены.")


class ProductDetailView(DetailView):
    """Класс просмотра деталей продукта."""
    model = Product
    # Новая страница с формой
    template_name = 'catalog/product_detail.html'
    # Контекст передаваемый в шаблон
    context_object_name = 'product'


class ProductCreateView(CreateView):
    """Класс создания продукта."""
    model = Product
    # Указываем поля модели, которые будут в HTML-форме
    fields = ['name', 'purchase_price', 'description', 'category', 'picture',]
    # Новая страница с формой
    template_name = 'catalog/product_form.html'
    # Перенаправляем пользователя после успешного создания товара
    success_url = reverse_lazy('catalog:products_list')


class ProductUpdateView(UpdateView):
    """Класс обновления данных продукта."""
    model = Product
    # Указываем поля модели, которые будут в HTML-форме
    fields = ['name', 'purchase_price', 'description', 'category', 'picture']
    # Новая страница с формой
    template_name = 'catalog/product_form.html'
    # Перенаправляем пользователя после успешного создания товара
    success_url = reverse_lazy('catalog:products_list')


class ProductDeleteView(DeleteView):
    """Класс просмотра удаления продукта."""
    model = Product
    # Новая страница с формой
    template_name = 'catalog/product_confirm_delete.html'
    # Перенаправляем пользователя после успешного удаления товара
    success_url = reverse_lazy('catalog:products_list')
