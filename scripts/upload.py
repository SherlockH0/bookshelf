import os
from pprint import pprint

import cloudinary.uploader
from django.core.files import File

from bookshelf.settings import BASE_DIR

from .generate_images import INPUT_DIR, OUTPUT_DIR, generate

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bookshelf.settings")
import django

django.setup()

import pyperclip

SUFFIX = "Write a 2 paragraph book description (NO SPOILERS) in a bookshop using markdown for the book {0}\n"

from shop.models import Author, Book, Category, Genre

ERROR = "\033[91m"
SUCCESS = "\033[92m"
WARNING = "\033[93m"
UNDERLINE = "\033[4m"
ENDC = "\033[0m"


def upload_file_to_server(file_path):
    result = cloudinary.uploader.upload(file_path)
    return result["secure_url"]


import psycopg2

conn = psycopg2.connect()

cursor = conn.cursor()

cursor.execute("SELECT slug FROM shop_book")
image_files = set(i[0] for i in cursor.fetchall())

while True:
    input_images = set(os.path.splitext(i)[0] for i in os.listdir(BASE_DIR / INPUT_DIR))

    difference = image_files - input_images
    if difference:
        print(
            WARNING,
            "Please, add covers for the books listed bellow into a 'images_input' folder and press enter to continue:",
            ENDC,
        )
        print("\n".join(difference))
        input()

    else:
        break

generate(BASE_DIR)

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

    slug = book[8]
    about = book[2]

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
            # pyperclip.copy(SUFFIX.format(f"{name} by {author_name}"))
            # input(
            #     f"Description for the book {name} was added to your clipboard. Copy new description and press Enter to continue:"
            # )
            # about = pyperclip.paste()
            book = Book(
                name=name,
                about=about,
                genre=Genre.objects.get(name=genre_name),
                author=Author.objects.get(name=author_name),
                price=book[3],
            )
            book.image = upload_file_to_server(
                BASE_DIR / OUTPUT_DIR / f"{slug}_cover.webp"
            )
            book.image_preview = upload_file_to_server(
                BASE_DIR / OUTPUT_DIR / f"{slug}_preview.webp"
            )
            book.save()
            print(f"{SUCCESS}Added {name}")
    except Exception as e:
        print(f"{ERROR}Error adding {name}: {e}\n {UNDERLINE}{name} was not added")
    finally:
        print(ENDC)
