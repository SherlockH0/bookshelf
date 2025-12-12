from random import randint
from typing import TYPE_CHECKING, Union

from django.db.models import Q
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import DetailView, ListView

from utils.shop_data import OrderData, WishlistData

from .models import Author, Book, Genre

if TYPE_CHECKING:
    from django.db.models import BaseManager


def about(request: HttpRequest):
    return render(request, "shop/about.html")


def contacts(request: HttpRequest):
    return render(request, "shop/contacts.html")


def home(request: HttpRequest):
    books = Book.objects.all()

    query: str = request.GET.get("search", "")
    if query:
        context: dict[str, Union[str, BaseManager[Book]]] = {
            "books": books.filter(
                Q(name__icontains=query)
                | Q(author__name__icontains=query)
                | Q(about__icontains=query)
                | Q(genre__name__icontains=query)
            ),
            "query": query,
        }

        return render(request, "shop/search_results.html", context)

    pks = books.count()
    if not pks:
        return render(request, "shop/home.html")
    random_pk = randint(0, pks - 1)
    random_book = str(books[random_pk])
    display = books.filter(on_display=True)[:2]
    bestsellers = books.filter(is_bestseller=True)[:3]

    context = {
        "books": books,
        "random_book": random_book,
        "display": display,
        "bestsellers": bestsellers,
    }

    return render(request, "shop/home.html", context)


class BookListView(ListView):
    model = Book

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        slug = self.kwargs.get("slug")
        keyword = "author"
        CategoryModel = Author

        if self.request.path == reverse("shop-books-genre", kwargs={"slug": slug}):
            CategoryModel = Genre
            keyword = "genre"

        filter_obj = get_object_or_404(CategoryModel, slug=slug)

        context["description"] = filter_obj
        context["object_list"] = Book.objects.filter(**{keyword: filter_obj})

        return context


class BookDetailView(DetailView):
    model = Book

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["cart_items"] = OrderData(self.request).order.get_item_ids()
        context["wishlist_items"] = WishlistData(self.request).wishlist.get_item_ids()
        return context
