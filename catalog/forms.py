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


class ProductUserForm(forms.ModelForm):
    """Родительская форма пользователя со ВСЕМИ полями и полной валидацией."""
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
        # Возможно вместо fields написать exclude = ("  поле","поле") то есть написать исключаемые поля
        fields = ['name', 'purchase_price', 'description', 'category', 'owner', 'picture']

    def __init__(self, *args, **kwargs):
        super(ProductUserForm, self).__init__(*args, **kwargs)

        # Принудительно задаем класс Bootstrap для списка ошибок каждого поля
        self.error_class = BootstrapErrorList

        # Автоматически добавляем Bootstrap-класс 'form-control' для ВСЕХ полей
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

        # Добавляем индивидуальные подсказки (placeholder)
        self.fields['name'].widget.attrs.update({'placeholder': 'Введите имя'})
        self.fields['description'].widget.attrs.update({'placeholder': 'Введите описание продукта'})
        self.fields['category'].widget.attrs.update({'placeholder': 'Выберите категорию продукта'})

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


class ProductModeratorForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['publication_status']  # Модератор видит одно поле

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_class = BootstrapErrorList
        self.fields['publication_status'].widget.attrs.update({'class': 'form-control'})