from django.db import models
from django.template.defaultfilters import slugify

# Create your models here.


class Author(models.Model):

    name = models.CharField(max_length=50)
    portrait = models.ImageField(
        default='default_author.jpeg',
        upload_to='author_portraits')
    about = models.TextField()
    slug = models.SlugField(default="", null=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class Category(models.Model):

    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Genre(models.Model):

    name = models.CharField(max_length=50)
    about = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    slug = models.SlugField(default="", null=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class Book(models.Model):

    name = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    about = models.TextField()
    price = models.FloatField()
    image = models.ImageField(default='default.jpeg', upload_to='book_covers')
    date_created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(default="", null=False)

    def __str__(self):
        return f'{self.name} by {self.author}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
