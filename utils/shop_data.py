from orders.models import *
from shop.models import Book
import json


def get_cookie(cookies, name):
    return json.loads(cookies[name]) if name in cookies.keys() else {}


def safe_get(model, id):
    try:
        return model.objects.get(
            id=id)
    except Exception:
        print(Exception)
        return None


def get_book(book):
    return {
        'id': book.id,
        'name': book.name,
        'author': book.author,
        'price': book.price,
        'image': book.image,
        'image_preview': book.image_preview,
        'slug': book.slug
    }


class CookieModel:
    def get_item_count(self):
        return self.item_count

    def get_item_ids(self):
        return [item['book']['id'] for item in self.items]


class CookieOrder(CookieModel):

    def __init__(self, cart):
        self.items = []
        self.item_count = 0
        self.total = 0
        for i in cart:
            if (book := safe_get(Book, i)) is None:
                continue

            quantity = cart[i]['quantity']
            self.item_count += quantity
            self.total += book.price * quantity

            self.items.append({
                'book': get_book(book),
                'quantity': quantity,
                'date_added': cart[i]['date_added']
            })

    def get_total(self):
        return self.total


class CookieWishlist(CookieModel):

    def __init__(self, wishlist):
        self.items = []
        self.item_count = 0
        self.total = 0
        for i in wishlist:
            if (book := safe_get(Book, i)) is None:
                continue

            self.item_count += 1

            self.items.append({
                'book': get_book(book),
                'date_added': wishlist[i]['date_added']
            })


class ModelData:
    """Basic class for data.
    If user is not authenticated, data is taken from cookies.
    Items are sortd by date added"""

    def __init__(self, request):
        self.user = request.user
        self.request = request

        if self.user.is_authenticated:
            self.auth_init()
            self.items = self.items.order_by('-date_added')
        else:
            cookies = request.COOKIES
            self.cookie_init(cookies)
            self.items = sorted(
                self.items,
                key=lambda item: -item['date_added'])

class OrderData(ModelData):

    def auth_init(self):
        self.order, c = Order.objects.get_or_create(
            customer=self.user.customer, complete=False)
        self.items = self.order.orderitem_set.all()

    def cookie_init(self, cookies):
        cart = get_cookie(cookies, 'cart')

        self.order = CookieOrder(cart)
        self.items = self.order.items

    def get_real(self, customer):
        if self.user.is_authenticated:
            self.order.customer = customer
            return self.order

        order = Order.objects.create(
            customer=customer, complete=False)

        for i in self.items:
            book = safe_get(Book, i['book']['id'])

            OrderItem.objects.create(
                book=book,
                order=order,
                quantity=i['quantity']
            )
        return order


class WishlistData(ModelData):
    def auth_init(self):
        self.wishlist, c = Wishlist.objects.get_or_create(
            customer=self.user.customer)
        self.items = self.wishlist.wishlistitem_set.all()

    def cookie_init(self, cookies):
        wishlist = get_cookie(cookies, 'wishlist')

        self.wishlist = CookieWishlist(wishlist)
        self.items = self.wishlist.items
