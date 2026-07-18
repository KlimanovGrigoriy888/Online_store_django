import re
import os
from django import forms
from django.core.exceptions import ValidationError
from django.forms.utils import ErrorList

from .models import Product


class BootstrapErrorList(ErrorList):
    """Вспомогательный класс для создания стиля ошибок"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Добавляем класс 'text-danger' (красный текст) или 'alert alert-danger'
        self.error_class = 'text-danger small d-block mt-1'


class ProductForm(forms.ModelForm):
    # Список запретных слов объявленных во множестве
    BAD_WORDS = {'казино',
                 'криптовалюта',
                 'крипта',
                 'биржа',
                 'дешево',
                 'бесплатно',
                 'обман',
                 'полиция',
                 'радар'}

    class Meta:
        model = Product
        fields = ['name', 'purchase_price', 'description', 'category', 'picture', ]

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)

        # Принудительно задаем класс Bootstrap для списка ошибок каждого поля
        self.error_class = BootstrapErrorList

        # Настройка атрибутов виджета для поля 'first_name'
        self.fields['name'].widget.attrs.update({
            'class': 'form-control',  # Добавление CSS-класса для стилизации поля
            'placeholder': 'Введите имя'  # Текст подсказки внутри поля
        })

        # Настройка атрибутов виджета для поля 'purchase_price'
        self.fields['purchase_price'].widget.attrs.update({
            'class': 'form-control',  # Добавление CSS-класса для стилизации поля
        })

        # Настройка атрибутов виджета для поля 'description'
        self.fields['description'].widget.attrs.update({
            'class': 'form-control',  # Добавление CSS-класса для стилизации поля
            'placeholder': 'Введите описание продукта'  # Текст подсказки внутри поля
        })

        # Настройка атрибутов виджета для поля 'category'
        self.fields['category'].widget.attrs.update({
            'class': 'form-control',  # Добавление CSS-класса для стилизации поля
            'placeholder': 'Выберите категорию продукта'  # Текст подсказки внутри поля
        })

        # Настройка атрибутов виджета для поля 'picture'
        self.fields['picture'].widget.attrs.update({
            'class': 'form-control',  # Добавление CSS-класса для стилизации поля
        })

    # Метод валидации поля purchase_price, что цена продукта не может быть отрицательной.
    # Название метода должно включать название поля, иначе не работает
    def clean_purchase_price(self):
        price = self.cleaned_data.get('purchase_price')

        # Проверяем, что цена не отрицательная
        if price is not None and price < 0:
            raise forms.ValidationError("Цена продукта не может быть отрицательной.")

        return price

    def clean_picture(self):
        picture = self.cleaned_data.get('picture')

        # Если пользователь не загрузил картинку (а поле необязательное), пропускаем проверку
        if not picture:
            return picture

        # 1. Валидация размера (5 МБ = 5 * 1024 * 1024 байт)
        max_size = 5 * 1024 * 1024
        if picture.size > max_size:
            raise ValidationError("Размер файла не должен превышать 5 МБ.")

        # 2. Валидация формата (по расширению файла)
        ext = os.path.splitext(picture.name)[1].lower()
        valid_extensions = ['.jpg', '.jpeg', '.png']
        if ext not in valid_extensions:
            raise ValidationError("Допускаются только изображения в формате JPEG или PNG.")

        return picture

    # Метод валидации полей name и description на запретные слова
    def clean(self):
        # получаем очищенные данные всей формы
        cleaned_data = super().clean()

        # Список полей которые нужно проверить на запретные слова
        field_to_check = ['name', 'description']

        # Перебираем поля циклом
        for field_name in field_to_check:
            # Извлекаем поле из cleaned_data
            text = cleaned_data.get(field_name)

            if not text:
                continue  # Пропуск если поле пустое или не прошло базовую валидацию
            # используем фильтр для извлечения только слов без точек, запятых и пробелов, слова приводим к нижнему
            # регистру
            words_in_text = re.findall(r'\b\w+\b', text.lower())

            # Проверяем есть запрещенное слово в тексте с помощью метода проверки пересечения слов во множествах
            found_bad_words = self.BAD_WORDS.intersection(words_in_text)

            if found_bad_words:
                # Берем первое найденное слово для вывода в ошибку
                bad_word = list(found_bad_words)[0]
                # Привязываем ошибку к конкретному полю формы
                self.add_error(field_name, forms.ValidationError(f'Текст содержит запрещенное слово {bad_word}!'))

        return cleaned_data
