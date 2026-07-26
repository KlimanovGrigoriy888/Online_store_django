from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core.mail import send_mail  # Импортируем функцию отправки почты
from config import settings  # Импортируем настройки, чтобы взять EMAIL
from blog.models import BlogEntry
from django.urls import reverse


class BlogListView(ListView):
    """Класс просмотра всех блоговых записей."""
    model = BlogEntry
    # Новый шаблон страницы для просмотра всех продуктов
    template_name = 'blog/blog_list.html'
    # Контекст передаваемый в шаблон
    context_object_name = 'blogs'

    def get_queryset(self):
        # Получаем список статей из Базы данных с помощью get_queryset только те, которые имеют положительный признак
        # публикации.
        # Метод из примера в конспекте BlogEntry.objects.filter(is_published=True)
        return super().get_queryset().filter(is_published=True)


class BlogDetailView(DetailView):
    """Класс просмотра деталей блоговой записей."""
    model = BlogEntry
    # Новая страница с формой
    template_name = 'blog/blog_detail.html'
    # Контекст передаваемый в шаблон
    context_object_name = 'blog'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()

        # Проверяем: если это ровно 100-й просмотр
        if self.object.views_count == 12:
            # Пересылка на email при срабатывании условия счетчика
            send_mail(
                subject='Поздравляем с достижением!',
                message=f'Ваша статья "{self.object.title}" набрала 100 просмотров! Отличный результат!',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=['Grigorij31@yandex.com'],  # Укажите здесь свою почту
                fail_silently=False,
            )

        return self.object


class BlogCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Класс создания блоговой записи."""
    model = BlogEntry
    # Указываем поля модели, которые будут в HTML-форме
    fields = ['title', 'content', 'preview', 'is_published']
    # Новая страница с формой
    template_name = 'blog/blog_form.html'
    # Перенаправляем пользователя после успешного создания товара
    success_url = reverse_lazy('blog:blog_list')
    # Добавление ограничения для пользователей
    permission_required = 'blog.add_blogentry'


class BlogUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Класс изменения блоговой записи."""
    model = BlogEntry
    # Указываем поля модели, которые будут в HTML-форме
    fields = ['title', 'content', 'preview', 'is_published']
    # Новая страница с формой
    template_name = 'blog/blog_form.html'
    # Добавление ограничения для пользователей
    permission_required = 'blog.change_blogentry'
    # # Перенаправляем пользователя после успешного создания товара не работает, необходимо применить
    # # get_success_url(self):
    # success_url = reverse_lazy('blog:blog_detail')

    def get_success_url(self):
        """Динамически перенаправляет на страницу просмотра измененной статьи."""
        # self.object — это та самая статья, которую мы только что сохранили
        return reverse('blog:blog_detail', args=[self.kwargs.get('pk')])


class BlogDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Класс просмотра удаления блоговой записи."""
    model = BlogEntry
    # Новая страница с формой
    template_name = 'blog/blog_confirm_delete.html'
    # Перенаправляем пользователя после успешного удаления товара
    success_url = reverse_lazy('blog:blog_list')
    # Добавление ограничения для пользователей
    permission_required = 'blog.delete_blogentry'
