from shop.models import Genre

from .shop_data import OrderData, WishlistData


def navbar_info(request):
    genres = Genre.objects.select_related("category").order_by("category")

    cart_item_count = OrderData(request).order.get_item_count()
    wishlist_item_count = WishlistData(request).wishlist.get_item_count()

    return {
        "genres": genres,
        "cart_item_count": cart_item_count,
        "wishlist_item_count": wishlist_item_count,
    }
