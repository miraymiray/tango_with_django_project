from django.http import HttpResponse
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm
from django.urls import reverse
from django.shortcuts import redirect, render

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

def add_category(request):
    form = CategoryForm()

    # A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)

            # Redirect the user back to the index view.
            return redirect('/rango/')
        else:
            # The supplied form contained errors - just print them to the terminal.
            print(form.errors)

    # Will handle the bad form, new form, or no form supplied cases.
    # Render the form with error messages (if any).
    return render(request, 'rango/add_category.html', {'form': form})

def add_page(request, category_name_slug):
    """
    Handles adding a new page to a specific category.
    """
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    # If category does not exist, redirect to the homepage
    if category is None:
        return redirect('/rango/')

    form = PageForm()

    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            page = form.save(commit=False)
            page.category = category
            page.views = 0
            page.save()
            return redirect(reverse('rango:show_category', kwargs={'category_name_slug': category_name_slug}))
        else:
            print(form.errors)

    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context=context_dict)