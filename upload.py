import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bookshelf.settings")
import django
django.setup()

from shop.models import Book, Genre, Author
import json


class bcolors:
    ERROR = '\033[91m'
    SUCCESS = '\033[92m'
    WARNING = '\033[93m'
    UNDERLINE = '\033[4m'
    ENDC = '\033[0m'


with open("authors.json") as f:
    authors_json = json.load(f)

for author in authors_json:
    name = author['name']

    try:
        if Author.objects.filter(name=name).exists():
            print(f'{bcolors.WARNING}{name} is already in database and {bcolors.UNDERLINE}was not added')
        else:
            author = Author(name=name, about=author['about'])
            author.save()
            print(f'{bcolors.SUCCESS}Added {name}')
    except Exception as e:
        print(f'{bcolors.ERROR}Error adding {name}: {e} \n {bcolors.UNDERLINE}{name} was not added')
    finally:
        print(bcolors.ENDC)


with open("books.json") as f:
    books_json = json.load(f)

for book in books_json:
    name = book['title']
    genre_name = book['genre']
    author_name = book['author']

    if not Genre.objects.filter(name=genre_name).exists():
        print(f'{bcolors.ERROR}Genre with name {genre_name} does not exist. {bcolors.UNDERLINE}{name} was not added{bcolors.ENDC}')
        continue
    elif not Author.objects.filter(name=author_name).exists():
        print(f'{bcolors.ERROR}Author with name {author_name} does not exist. {bcolors.UNDERLINE}{name} was not added{bcolors.ENDC}')
        continue

    try:
        if Book.objects.filter(name=name).exists():
            print(f'{bcolors.WARNING}{name} is already in database and {bcolors.UNDERLINE}was not added')
        else:
            book = Book(
                name=name,
                about=book['about'],
                genre=Genre.objects.get(name=genre_name),
                author=Author.objects.get(name=author_name),
                price=book['price'])
            book.save()
            print(f'{bcolors.SUCCESS}Added {name}')
    except Exception as e:
        print(f'{bcolors.ERROR}Error adding {name}: {e}\n {bcolors.UNDERLINE}{name} was not added')
    finally:
        print(bcolors.ENDC)
