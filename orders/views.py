import datetime
import json

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render

from orders.models import *
from shop.models import Book
from utils.shop_data import OrderData, WishlistData

# Create your views here.


def cart(request):
    data = OrderData(request)

    return render(
        request, "orders/cart.html", {"order": data.order, "items": data.items}
    )


def wishlist(request):
    data = WishlistData(request)

    context = {"items": data.items}
    return render(request, "orders/wishlist.html", context)


def checkout(request):
    data = OrderData(request)
    return render(
        request, "orders/checkout.html", {"order": data.order, "items": data.items}
    )


def update_item(request):
    data = json.loads(request.body)
    bookId = data["bookId"]
    action = data["action"]
    place = data["place"]

    customer = request.user.customer
    book = Book.objects.get(id=bookId)

    if place == "cart":
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

        item, created = OrderItem.objects.get_or_create(order=order, book=book)

    elif place == "wishlist":
        wishlist, created = Wishlist.objects.get_or_create(customer=customer)

        item, created = WishlistItem.objects.get_or_create(wishlist=wishlist, book=book)

    if action == "delete":
        item.delete()

    elif action.startswith("set-to-"):
        if (quantity := action.replace("set-to-", "")).isdigit():
            item.quantity = int(quantity)
            item.save()

    return JsonResponse(f"item was {action}", safe=False)


def process_order(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    order_data = OrderData(request)

    first_name = data["form"]["first_name"]
    last_name = data["form"]["last_name"]
    email = data["form"]["email"]

    customer, created = Customer.objects.get_or_create(email=email)
    customer.first_name = first_name
    customer.last_name = last_name
    customer.save()

    order = order_data.get_real(customer)
    total = float(data["form"]["total"])
    order.transaction_id = transaction_id

    if total == order.get_total():
        order.complete = True
        messages.success(request, "Transaction complete successfuly")
    else:
        messages.error(request, "Sorry, something went wrong :(")
    order.save()

    ShippingDetails.objects.create(
        customer=customer,
        order=order,
        adress=data["shipping"]["adress"],
        city=data["shipping"]["city"],
        country=data["shipping"]["country"],
        postal_code=data["shipping"]["postal_code"],
    )

    return JsonResponse("Payment complete!", safe=False)
