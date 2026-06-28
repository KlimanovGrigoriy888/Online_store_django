from django.db import models


class BlogEntry(models.Model):
    """Класс создания блога"""

    title = models.CharField(max_length=150, verbose_name='Заголовок', help_text="Укажите заголовок", )
    content = models.TextField(verbose_name='Содержимое', help_text="Напишите содержание", )
    preview = models.ImageField(upload_to='blog_previews/', verbose_name='Изображение', blank=True, null=True,
                                help_text="Загрузите изображение продукта", )
    created_at = models.DateField(auto_now_add=True, verbose_name='Дата создания', )
    is_published = models.BooleanField(default=True, verbose_name='Признак публикации')
    views_count = models.IntegerField(default=0, verbose_name='Количество просмотров', )

    def __str__(self):
        return f'{self.title} Количество просмотров: {self.views_count}'

    class Meta:
        verbose_name = 'Блоговая запись'
        verbose_name_plural = 'Блоговые записи'
        ordering = ['created_at', ]
