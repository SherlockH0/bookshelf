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
