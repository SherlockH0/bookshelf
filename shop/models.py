from django.db import models
from django.template.defaultfilters import slugify

# Create your models here.


class Author(models.Model):

    name = models.CharField(max_length=50)
    portrait = models.ImageField(
        default='default_author.jpeg',
        upload_to='author_portraits')
    about = models.TextField()
    slug = models.SlugField(default="", null=True, blank=True)

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class Category(models.Model):

    name = models.CharField(max_length=50)

    def __str__(self):
        return str(self.name)


class Genre(models.Model):

    name = models.CharField(max_length=50)
    about = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    slug = models.SlugField(default="", null=True, blank=True)

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

class BookManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related("author", "genre")

class Book(models.Model):

    name = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    about = models.TextField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    image_preview = models.ImageField(help_text="height 310px",  upload_to='book_covers', null=True, blank=True)
    image = models.ImageField(help_text="width 300px",  upload_to='book_covers', null=True, blank=True)
    date_created = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=100, default="", null=True, blank=True)

    objects = BookManager()

    def __str__(self):
        return f'{self.name} by {self.author}'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
