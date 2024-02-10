from django.db import models
from django.contrib.auth.models import AbstractUser
from django.template.defaultfilters import slugify


# Create your models here.

class User(AbstractUser):
    username = models.CharField(db_index=True, unique=True, max_length=255)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def save(self, *args, **kwargs):
        self.username = slugify(self.email)
        super().save(*args, **kwargs)

        customer, created = Customer.objects.get_or_create(user=self)
        customer.first_name = self.first_name
        customer.last_name = self.last_name
        customer.email = self.email
        customer.save()


class Customer(models.Model):
    user = models.OneToOneField(
        User,
        default=None,
        on_delete=models.SET_DEFAULT,
        null=True,
        blank=True)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    email = models.EmailField()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
