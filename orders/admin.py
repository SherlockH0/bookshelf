from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Wishlist)
admin.site.register(WishlistItem)
admin.site.register(ShippingDetails)
