import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bookshelf.settings")
import django
django.setup()

from shop.models import Book, Genre, Author, Category
import json


ERROR = '\033[91m'
SUCCESS = '\033[92m'
WARNING = '\033[93m'
UNDERLINE = '\033[4m'
ENDC = '\033[0m'


with open("db.json") as f:
    db = json.load(f)

print(f'{WARNING}{"-"*20}ADDING AUTHORS{"-"*20}{ENDC}')

for author in db['authors']:
    name = author['name']

    try:
        if Author.objects.filter(name=name).exists():
            print(
                f'{WARNING}{name} is already in database and {UNDERLINE}was not added')
        else:
            author = Author(name=name, about=author['about'])
            author.save()
            print(f'{SUCCESS}Added {name}')
    except Exception as e:
        print(f'{ERROR}Error adding {name}: {e} \n {UNDERLINE}{name} was not added')
    finally:
        print(ENDC)

print(f'{WARNING}{"-"*20}ADDING GENRES{"-"*20}{ENDC}')

for genre in db['genres']:
    name = genre['name']
    category = genre['category']

    if not Category.objects.filter(name=category).exists():
        print(f'{ERROR}Category with name {category} does not exist. {UNDERLINE}{name} was not added{ENDC}')
        continue

    try:
        if Genre.objects.filter(name=name).exists():
            print(
                f'{WARNING}{name} is already in database and {UNDERLINE}was not added')
        else:
            genre = Genre(
                name=name,
                about=genre['about'],
                category=Category.objects.get(name=category),)
            genre.save()
            print(f'{SUCCESS}Added {name}')
    except Exception as e:
        print(f'{ERROR}Error adding {name}: {e} \n {UNDERLINE}{name} was not added')
    finally:
        print(ENDC)

print(f'{WARNING}{"-"*20}ADDING BOOKS{"-"*20}{ENDC}')

for book in db['books']:
    name = book['name']
    genre_name = book['genre']
    author_name = book['author']

    if not Genre.objects.filter(name=genre_name).exists():
        print(
            f'{ERROR}Genre with name {genre_name} does not exist. {UNDERLINE}{name} was not added{ENDC}')
        continue
    elif not Author.objects.filter(name=author_name).exists():
        print(f'{ERROR}Author with name {author_name} does not exist. {UNDERLINE}{name} was not added{ENDC}')
        continue

    try:
        if Book.objects.filter(name=name).exists():
            print(
                f'{WARNING}{name} is already in database and {UNDERLINE}was not added')
        else:
            book = Book(
                name=name,
                about=book['about'],
                genre=Genre.objects.get(name=genre_name),
                author=Author.objects.get(name=author_name),
                price=book['price'])
            book.save()
            print(f'{SUCCESS}Added {name}')
    except Exception as e:
        print(f'{ERROR}Error adding {name}: {e}\n {UNDERLINE}{name} was not added')
    finally:
        print(ENDC)
