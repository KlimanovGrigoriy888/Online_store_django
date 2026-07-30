from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden
from django.urls import reverse_lazy

from .forms import ProductUserForm, ProductModeratorForm
from .models import Product
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView, DetailView, DeleteView, View


class ProductListView(ListView):
    """Класс просмотра всех продуктов."""
    model = Product
    # Новый шаблон страницы для просмотра всех продуктов
    template_name = 'catalog/products_list.html'
    # Контекст передаваемый в шаблон
    context_object_name = 'products'

    def get_queryset(self):
        """Здесь выводим в консоль 5 последних товаров из БД."""
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


class ProductCreateView(LoginRequiredMixin, CreateView):
    """Класс создания продукта с записью пользователя при создании продукта."""
    model = Product
    # Указываем поля модели, которые будут в HTML-форме
    # fields = ['name', 'purchase_price', 'description', 'category', 'picture',]
    # Для получения данных с входной формы HTML шаблона указываем класс формы для работы через формы
    form_class = ProductUserForm
    # Новая страница с формой
    template_name = 'catalog/product_form.html'
    # Перенаправляем пользователя после успешного создания товара
    success_url = reverse_lazy('catalog:products_list')

    def form_valid(self, form):
        """Метод записывающий текущего пользователя продукта в БД """
        product = form.save()  # Django берет данные из формы и сохраняет в базе
        # получаем текущего пользователя из сессии
        user = self.request.user
        # пишем текущего пользователя в БД как owner
        product.owner = user
        # сохраняем пользователя в БД
        product.save()
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """Класс обновления данных продукта с проверкой на регистрацию пользователя и наличия права на изменение
    статуса публикации товара."""
    model = Product
    # Указываем поля модели, которые будут в HTML-форме
    # fields = ['name', 'purchase_price', 'description', 'category', 'picture']
    # Для получения данных с входной формы HTML шаблона указываем класс формы для работы через формы
    form_class = ProductUserForm
    # Новая страница с формой
    template_name = 'catalog/product_form.html'
    # Перенаправляем пользователя после успешного создания товара
    success_url = reverse_lazy('catalog:products_list')

    def get_form_class(self):
        """Функция изменения формы на форму модератора при наличии прав модератора или создателя продукта"""
        #  Получаем данные пользователя из текущей сессии
        user = self.request.user
        # Если пользователь владелец (создатель) продукта (получено из формы), возвращаем стандартную форму
        if user == self.object.owner:
            return ProductUserForm

        # Если зашел модератор (проверяем его право) — даем форму только для статуса
        if user.has_perm('catalog.can_unpublish_product'):
            # Возвращаем форму модератора
            return ProductModeratorForm

        # Если зашел чужой пользователь — доступ запрещен
        raise PermissionDenied


class ProductDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Класс просмотра удаления продукта с проверкой на регистрацию пользователя и наличия права разрешения на
    удаления продукта."""
    model = Product
    # Новая страница с формой
    template_name = 'catalog/product_confirm_delete.html'
    # Перенаправляем пользователя после успешного удаления товара
    success_url = reverse_lazy('catalog:products_list')
    # Проверка наличия разрешения на удаление продукта
    # permission_required = 'catalog.delete_product' удалили так как сделали доп проверку на owner-создателя продукта

    def dispatch(self, request, *args, **kwargs):
        """Функция проверки, что пользователь создатель продукта и имеет права на удаление продукта """
        # Получаем данные продукта из БД
        product = self.get_object()
        # Получаем данные о текущем пользователе из текущей сессии
        user = request.user
        # Проверка, что пользователь владелец продукта и имеет права на удаление продукта
        is_owner = (user == product.owner)
        is_moderator = user.has_perm('catalog.delete_product')

        # Если НЕ владелец и НЕ модератор — закрываем доступ
        if not (is_owner or is_moderator):
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)

