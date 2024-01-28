from django.shortcuts import render
from orders.models import *
from shop.models import Book
from django.http import JsonResponse
import json
import datetime

# Create your views here.


def cart(request):

    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(
            customer=request.user.customer, complete=False)

        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_total': 0, 'get_items': 0}

    return render(request, 'orders/cart.html',
                  {'order': order,
                   'items': items})


def wishlist(request):

    if request.user.is_authenticated:
        wishlist, created = Wishlist.objects.get_or_create(
            customer=request.user.customer)

        items = wishlist.wishlistitem_set.all()
        books = Book.objects.filter(id__in=items.values_list('book'))
    else:
        books = []

    context = {'books': books}
    return render(
        request,
        'orders/wishlist.html',
        context)


def checkout(request):

    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(
            customer=request.user.customer, complete=False)

        items = order.orderitem_set.all()
    else:
        items = []

    return render(request, 'orders/checkout.html', {'items': items})


def update_item(request):
    data = json.loads(request.body)
    bookId = data['bookId']
    action = data['action']
    place = data['place']

    print('Book:', bookId)
    print('Action:', action)
    print('Place:', place)

    customer = request.user.customer
    book = Book.objects.get(id=bookId)

    if place == 'cart':

        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)

        item, created = OrderItem.objects.get_or_create(
            order=order, book=book)

    elif place == 'wishlist':

        wishlist, created = Wishlist.objects.get_or_create(
            customer=customer)

        item, created = WishlistItem.objects.get_or_create(
            wishlist=wishlist, book=book)

    if action == 'delete':
        item.delete()

    elif action.startswith('set-to-'):
        quantity = action.replace('set-to-', '')
        print(quantity)
        if quantity.isdigit():
            item.quantity = int(quantity)
            item.save()

    return JsonResponse(f'item was {action}', safe=False)


def process_order(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_total():
            order.complete = True
        order.save()

        ShippingDetails.objects.create(
            customer=customer,
            order=order,
            adress=data['shipping']['adress'],
            city=data['shipping']['city'],
            country=data['shipping']['country'],
            postal_code=data['shipping']['postal_code']
        )

    else:
        print('User is not authenticated')
    return JsonResponse('Payment complete!', safe=False)
