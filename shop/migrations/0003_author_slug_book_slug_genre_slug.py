# Generated by Django 4.2.3 on 2024-01-24 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_remove_author_slug_remove_book_slug_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='slug',
            field=models.SlugField(default='', null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='slug',
            field=models.SlugField(default='', null=True),
        ),
        migrations.AddField(
            model_name='genre',
            name='slug',
            field=models.SlugField(default='', null=True),
        ),
    ]
