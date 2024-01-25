from django.shortcuts import render
from orders.models import Order, Wishlist

# Create your views here.


def cart(request):

    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(
            customer=request.user.customer, complete=False)

        items = order.orderitem_set.all()
    else:
        items = []

    return render(request, 'orders/cart.html', {'items': items})


def wishlist(request):

    if request.user.is_authenticated:
        wishlist, created = Wishlist.objects.get_or_create(
            customer=request.user.customer)

        items = wishlist.wishlistitem_set.all()
    else:
        items = []

    return render(
        request,
        'orders/wishlist.html',
        {'object_list': items})
