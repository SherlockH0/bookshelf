from django.urls import path
from .views import BookListView, BookDetailView
from . import views

urlpatterns = [
    path('', views.home, name='shop-home'),
    path('about/', views.about, name='shop-about'),
    path(
        'genre/<slug:slug>/',
        BookListView.as_view(),
        name="shop-books-genre"),
    path(
        'author/<slug:slug>/',
        BookListView.as_view(),
        name="shop-books-author"),
    path('book/<slug:slug>/', BookDetailView.as_view(), name="book-detail"),
]
