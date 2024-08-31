from cloudinary.models import CloudinaryField
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse

# Create your models here.


class Author(models.Model):

    name = models.CharField(max_length=50)
    portrait = models.ImageField(
        default="default_author.jpeg", upload_to="author_portraits"
    )
    about = models.TextField()
    slug = models.SlugField(default="", null=True, blank=True)

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("shop-books-author", args=[self.slug])


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

    def get_absolute_url(self):
        return reverse("shop-books-genre", args=[self.slug])


class BookManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related("author", "genre")
            .order_by("date_created")
        )


class Book(models.Model):

    name = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    about = models.TextField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    image_preview = CloudinaryField("image", help_text="height 310px")
    image = CloudinaryField("image", help_text="width 300px")
    date_created = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=100, default="", null=True, blank=True)
    on_display = models.BooleanField(default=False)

    objects = BookManager()

    def __str__(self):
        return f"{self.name} by {self.author}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("book-detail", args=[self.slug])
