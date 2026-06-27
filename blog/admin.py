from django.contrib import admin
from .models import BlogEntry


@admin.register(BlogEntry)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'preview')
    list_filter = ('title', )
    search_fields = ('title', 'content',)



