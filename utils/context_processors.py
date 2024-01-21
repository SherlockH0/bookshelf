from shop.models import Category, Genre


def navbar_genres(request):
    sections = []
    for category in Category.objects.all():

        sections.append(
            {'category': category.name,
             'genres': Genre.objects.filter(category=category).values('name')
             })

    return {'sections': sections}
