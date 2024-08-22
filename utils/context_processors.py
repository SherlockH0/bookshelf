from shop.models import Category, Genre

from .shop_data import OrderData, WishlistData


def navbar_info(request):
    sections = []
    for category in Category.objects.all():

        sections.append(
            {
                "category": category.name,
                "genres": Genre.objects.filter(category=category),
            }
        )

    cart_item_count = OrderData(request).order.get_item_count()
    wishlist_item_count = WishlistData(request).wishlist.get_item_count()

    return {
        "sections": sections,
        "cart_item_count": cart_item_count,
        "wishlist_item_count": wishlist_item_count,
    }
