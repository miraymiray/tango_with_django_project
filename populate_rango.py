import os
import django
import random

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project.settings')
django.setup()

from rango.models import Category, Page

def populate():
    python_pages = [
        {'title': 'Official Python Tutorial', 'url': 'http://docs.python.org/3/tutorial/', 'views': random.randint(5, 100)},
        {'title': 'How to Think like a Computer Scientist', 'url': 'http://www.greenteapress.com/thinkpython/', 'views': random.randint(5, 100)},
        {'title': 'Learn Python in 10 Minutes', 'url': 'http://www.korokithakis.net/tutorials/python/', 'views': random.randint(5, 100)}
    ]

    django_pages = [
        {'title': 'Official Django Tutorial', 'url': 'https://docs.djangoproject.com/en/2.1/intro/tutorial01/', 'views': random.randint(5, 100)},
        {'title': 'Django Rocks', 'url': 'http://www.djangorocks.com/', 'views': random.randint(5, 100)},
        {'title': 'How to Tango with Django', 'url': 'http://www.tangowithdjango.com/', 'views': random.randint(5, 100)}
    ]

    other_pages = [
        {'title': 'Bottle', 'url': 'http://bottlepy.org/docs/dev/', 'views': random.randint(5, 100)},
        {'title': 'Flask', 'url': 'http://flask.pocoo.org', 'views': random.randint(5, 100)}
    ]

    cats = {
        'Python': {'pages': python_pages, 'views': 15, 'likes': 56},
        'Django': {'pages': django_pages, 'views': 60, 'likes': 90},
        'Other Frameworks': {'pages': other_pages, 'views': 2, 'likes': 17}
    }

    for cat, cat_data in cats.items():
        c = add_category(cat, cat_data['views'], cat_data['likes'])
        for p in cat_data['pages']:
            add_page(c, p['title'], p['url'], p['views'])

    print("Database population complete!")

def add_page(cat, title, url, views=0):
    p, created = Page.objects.get_or_create(category=cat, title=title)
    p.url = url
    p.views = views
    p.save()
    return p

def add_category(name, views=0, likes=0):
    c, created = Category.objects.get_or_create(name=name, defaults={'views': views, 'likes': likes})
    return c

if __name__ == '__main__':
    print("Starting Rango population script...")
    populate()
