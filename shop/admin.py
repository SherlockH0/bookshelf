from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Category)


@admin.register(Author, Genre)
class SubCategoryAdmin(admin.ModelAdmin):
    # exclude = ['slug']
    search_fields = ['name']
    fields = ['name', 'about', 'slug']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    exclude = ['slug']
    search_fields = ['name', 'author__name', 'genre__name']
    list_display = ['name', 'author', 'genre', 'price']
