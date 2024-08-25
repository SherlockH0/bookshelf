import os
from pprint import pprint

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bookshelf.settings")
import django

django.setup()

import pyperclip

SUFFIX = "Expand this into 2 paragraphs book description (NO SPOILERS) in a bookshop using markdown\n"

from shop.models import Author, Book, Category, Genre

ERROR = "\033[91m"
SUCCESS = "\033[92m"
WARNING = "\033[93m"
UNDERLINE = "\033[4m"
ENDC = "\033[0m"

import psycopg2

conn = psycopg2.connect(
    database="verceldb",
    host="ep-quiet-field-a25uwpjl-pooler.eu-central-1.aws.neon.tech",
    user="default",
    password="ks2ByRw1dCMD",
    port="5432",
)

cursor = conn.cursor()
cursor.execute("SELECT * FROM shop_author")
authors = cursor.fetchall()

cursor.execute("SELECT * FROM shop_book")
books = cursor.fetchall()

cursor.execute("SELECT * FROM shop_genre")
genres = cursor.fetchall()

pprint(type(authors[0]))


print(f'{WARNING}{"-"*20}ADDING AUTHORS{"-"*20}{ENDC}')

for author in authors:
    name = author[1]

    try:
        if Author.objects.filter(name=name).exists():
            print(
                f"{WARNING}{name} is already in database and {UNDERLINE}was not added"
            )
        else:
            author = Author(name=name, about=author[3])
            author.save()
            print(f"{SUCCESS}Added {name}")
    except Exception as e:
        print(f"{ERROR}Error adding {name}: {e} \n {UNDERLINE}{name} was not added")
    finally:
        print(ENDC)

print(f'{WARNING}{"-"*20}ADDING GENRES{"-"*20}{ENDC}')

for genre in genres:
    name = genre[1]
    category_id = genre[3]

    if not Category.objects.filter(id=category_id).exists():
        print(
            f"{ERROR}Category with id {category_id} does not exist. {UNDERLINE}{name} was not added{ENDC}"
        )
        continue

    try:
        if Genre.objects.filter(name=name).exists():
            print(
                f"{WARNING}{name} is already in database and {UNDERLINE}was not added"
            )
        else:
            genre = Genre(
                name=name,
                about=genre[2],
                category=Category.objects.get(id=category_id),
            )
            genre.save()
            print(f"{SUCCESS}Added {name}")
    except Exception as e:
        print(f"{ERROR}Error adding {name}: {e} \n {UNDERLINE}{name} was not added")
    finally:
        print(ENDC)
#
print(f'{WARNING}{"-"*20}ADDING BOOKS{"-"*20}{ENDC}')

for book in books:
    name = book[1]
    genre_id = book[7]
    author_id = book[6]

    cursor.execute(f"SELECT * FROM shop_genre WHERE id={genre_id}")
    genre_name = cursor.fetchone()[1]

    cursor.execute(f"SELECT * FROM shop_author WHERE id={author_id}")
    author_name = cursor.fetchone()[1]

    if not Genre.objects.filter(name=genre_name).exists():
        print(
            f"{ERROR}Genre with name {genre_name} does not exist. {UNDERLINE}{name} was not added{ENDC}"
        )
        continue
    elif not Author.objects.filter(name=author_name).exists():
        print(
            f"{ERROR}Author with name {author_name} does not exist. {UNDERLINE}{name} was not added{ENDC}"
        )
        continue

    try:
        if Book.objects.filter(name=name).exists():
            print(
                f"{WARNING}{name} is already in database and {UNDERLINE}was not added"
            )
        else:
            pyperclip.copy(SUFFIX + book[2])
            input(
                f"Description for the book {name} was added to your clipboard. Copy new description and press Enter to continue:"
            )
            about = pyperclip.paste()
            book = Book(
                name=name,
                about=about,
                genre=Genre.objects.get(name=genre_name),
                author=Author.objects.get(name=author_name),
                price=book[3],
            )
            book.save()
            print(f"{SUCCESS}Added {name}")
    except Exception as e:
        print(f"{ERROR}Error adding {name}: {e}\n {UNDERLINE}{name} was not added")
    finally:
        print(ENDC)
