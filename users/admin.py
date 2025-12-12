from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Customer

admin.site.register(User, UserAdmin)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ["__str__", "email", "user"]
