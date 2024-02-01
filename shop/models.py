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
        return self.name

    def save(self, *args, **kwargs):
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
    slug = models.SlugField(default="", null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class Book(models.Model):

    name = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    about = models.TextField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    image = models.ImageField(
        default='https://m.media-amazon.com/images/I/81QPHl7zgbL._AC_UF1000,1000_QL80_.jpg', upload_to='book_covers')
    date_created = models.DateTimeField(auto_now=True)
    slug = models.SlugField(default="", null=True, blank=True)

    def __str__(self):
        return f'{self.name} by {self.author}'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
