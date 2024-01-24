from django.db import models
from django.template.defaultfilters import slugify

# Create your models here.

class SlugMixin:
    slug = models.SlugField(default="", null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class Author(SlugMixin, models.Model):

    name = models.CharField(max_length=50)
    portrait = models.ImageField(
        default='default_author.jpeg',
        upload_to='author_portraits')
    about = models.TextField()

    def __str__(self):
        return self.name


class Category(models.Model):

    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Genre(SlugMixin, models.Model):

    name = models.CharField(max_length=50)
    about = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Book(SlugMixin, models.Model):

    name = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    about = models.TextField()
    price = models.FloatField()
    image = models.ImageField(default='default.jpeg', upload_to='book_covers')
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} by {self.author}'
