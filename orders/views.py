from django.shortcuts import render
from shop.models import Book

# Create your views here.


def cart(request):
    return render(request, 'orders/cart.html')


def wishlist(request):
    return render(request, 'orders/wishlist.html', {'object_list': Book.objects.all()})
