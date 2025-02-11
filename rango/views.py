from django.http import HttpResponse
from django.shortcuts import render
from rango.models import Category, Page

def index(request):
    category_list = Category.objects.order_by('-likes')[:5]  # Top 5 most liked categories
    page_list = Page.objects.order_by('-views')[:5]  # Top 5 most viewed pages

    context_dict = {
        'boldmessage': 'Crunchy, creamy, cookie, candy, cupcake!',
        'categories': category_list,
        'pages': page_list
    }

    return render(request, 'rango/index.html', context=context_dict)

def about(request):
    return render(request, 'rango/about.html')

def show_category(request, category_name_slug):
    # Create a context dictionary to pass to the template
    context_dict = {}

    try:
        # Try to get the category with the given slug
        category = Category.objects.get(slug=category_name_slug)

        # Retrieve associated pages
        pages = Page.objects.filter(category=category)

        # Add retrieved data to the context dictionary
        context_dict['pages'] = pages
        context_dict['category'] = category

    except Category.DoesNotExist:
        # If category doesn't exist, set values to None
        context_dict['category'] = None
        context_dict['pages'] = None

    # Render and return response
    return render(request, 'rango/category.html', context=context_dict)
