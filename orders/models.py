from django.db import models
from users.models import Customer
from shop.models import Book

# Create your models here.


class Order(models.Model):

    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)


class OrderItem(models.Model):

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.book.name


class Wishlist(models.Model):

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)


class WishlistItem(models.Model):

    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.book.name


class ShippingDetails(models.Model):

    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True)
    adress = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=255)
