from django.shortcuts import render
from django.db.models import Q
from .models import Book

def home(request):

    category = request.GET.get('category', 'all')

    if category == "all":
        books = Book.objects.all()
    else:
        books = Book.objects.filter(category=category)

    context = {
        "books": books,
        "category": category
    }

    return render(request, "home.html", context)

def home(request):

    query = request.GET.get('q')
    category = request.GET.get('category')

    books = Book.objects.all()

    # search filter
    if query:
        books = books.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(category__icontains=query)
        )

    # category filter
    if category and category != "all":
        books = books.filter(category=category)

    context = {
        'books': books,
        'query': query,
        'category': category
    }

    return render(request, 'home.html', context)