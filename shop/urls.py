from django.urls import path
from .views import BookListView, BookDetailView
from . import views

urlpatterns = [
    path('', views.home, name='shop-home'),
    path('genre/<str:genre>/', BookListView.as_view(), name="shop-books"),
    path('<int:pk>/', BookDetailView.as_view(), name="book-detail"),
]
