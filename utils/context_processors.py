from shop.models import Category, Genre
from orders.models import Order, Wishlist


def navbar_genres(request):
    sections = []
    for category in Category.objects.all():

        sections.append(
            {'category': category.name,
             'genres': Genre.objects.filter(category=category)
             })

    cart_items = 0
    cart_total = 0
    wishlist_items = 0

    if request.user.is_authenticated:
        customer = request.user.customer

        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        wishlist, created = Wishlist.objects.get_or_create(
            customer=customer)

        cart_items = order.get_items()
        cart_total = order.get_total()
        wishlist_items = wishlist.get_items()

    return {'sections': sections,
            'cart_items': cart_items,
            'cart_total': cart_total,
            'wishlist_items': wishlist_items}
