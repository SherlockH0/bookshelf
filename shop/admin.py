from django.contrib import admin

from .models import *

# Register your models here.

admin.site.register(Category)


@admin.register(Author, Genre)
class SubCategoryAdmin(admin.ModelAdmin):
    search_fields = ["name"]


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    search_fields = ["name", "author__name", "genre__name"]
    list_select_related = ["author", "genre"]
    list_display = ["name", "author", "genre", "price", "on_display"]
    list_editable = ["on_display", "price"]
    list_per_page = 10
