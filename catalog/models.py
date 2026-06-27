from django.db import models


class Category(models.Model):
    """Класс создания категории продукта"""

    name = models.CharField(max_length=150, verbose_name='наименование')
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return f'{self.name} {self.description}'

    class Meta:
        verbose_name = 'категория продукта'
        verbose_name_plural = 'категории продуктов'
        ordering = ['name', ]


class Product(models.Model):
    """Класс создания продукта"""

    name = models.CharField(max_length=150, verbose_name='Наименование', help_text="Укажите наименование продукта", )
    description = models.TextField(verbose_name='Описание', help_text="Напишите описание продукта", )
    picture = models.ImageField(upload_to='photos/', verbose_name='Изображение', blank=True, null=True,
                                help_text="Загрузите изображение продукта", )
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория', related_name='product',
                                 help_text="Укажите категорию продукта", )
    purchase_price = models.IntegerField(default=0, verbose_name='Цена за покупку', )
    created_at = models.DateField(auto_now_add=True, verbose_name='Дата создания', )
    updated_at = models.DateField(auto_now=True, verbose_name='дата последнего изменения', )

    def __str__(self):
        return f'{self.name} {self.description} {self.category}'

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'
        ordering = ['name', ]


class Contact(models.Model):
    """Класс создания контактов"""

    first_name = models.CharField(max_length=150, verbose_name='Имя')
    last_name = models.CharField(max_length=150, verbose_name='Фамилия')
    email = models.EmailField(verbose_name='Электронная почта')
    created_at = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateField(auto_now=True, verbose_name='дата последнего изменения')

    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.email}'

    class Meta:
        verbose_name = 'контакт'
        verbose_name_plural = 'контакты'
        ordering = ['first_name', 'last_name', ]
