from django.urls import path
from . import views

urlpatterns = [
    path('cart/', views.cart, name='cart'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('checkout/', views.checkout, name='checkout'),

    path('update_item/', views.update_item, name='update-item'),
    path('process_order/', views.process_order, name='process-order'),
]
