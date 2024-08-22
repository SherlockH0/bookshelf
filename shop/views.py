from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import DetailView, ListView

from utils.shop_data import OrderData, WishlistData

from .models import Author, Book, Genre


def about(request):
    return render(request, "shop/about.html")


def contacts(request):
    return render(request, "shop/contacts.html")


def home(request):
    # context = {'books': Book.objects.all().order_by('-date_created')[:15]}

    if "search" in request.GET and request.GET["search"] != "":
        query = request.GET["search"]
        context = {
            "books": Book.objects.filter(
                Q(name__icontains=query)
                | Q(author__name__icontains=query)
                | Q(about__icontains=query)
                | Q(genre__name__icontains=query)
            ),
            "query": query,
        }

        return render(request, "shop/search_results.html", context)

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
