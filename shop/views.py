from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Book, Genre
from django.db.models import Q


def about(request):
    return render(request, 'shop/about.html')


def home(request):
    context = {'books': Book.objects.all().order_by('-date_created')}

    if 'search' in request.GET and request.GET['search'] != '':
        query = request.GET['search']
        context = {
            'books': Book.objects.filter(
                Q(name__icontains=query)
                | Q(author__name__icontains=query)
                | Q(about__icontains=query)
                | Q(genre__name__icontains=query)),
            'query': query
        }

        return render(request, 'shop/search_results.html', context)

    return render(request, 'shop/home.html', context)


class BookListView(ListView):
    model = Book

    def get_queryset(self):

        genre = get_object_or_404(
            Genre,
            slug=self.kwargs.get('genre'))

        return Book.objects.filter(genre=genre)


class BookDetailView(DetailView):
    model = Book
