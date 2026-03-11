from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Book

# def home(request):

#     category = request.GET.get('category', 'all')

#     if category == "all":
#         books = Book.objects.all()
#     else:
#         books = Book.objects.filter(category=category)

#     context = {
#         "books": books,
#         "category": category
#     }

#     return render(request, "home.html", context)

from django.shortcuts import render
from .models import Book

def home(request):
    category = request.GET.get('category')

    if category:
        books = Book.objects.filter(category=category)
    else:
        books = Book.objects.all()

    context = {
        'books': books
    }

    return render(request, 'home.html', context)

def home(request):

    query = request.GET.get('q')
    category = request.GET.get('category')

    books = Book.objects.all()

    if query:
        books = books.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(category__icontains=query)
        )

   
    if category and category != "all":
        books = books.filter(category=category)

    context = {
        'books': books,
        'query': query,
        'category': category
    }

    return render(request, 'home.html', context)



def category_books(request, category_name):

    books = Book.objects.filter(category=category_name)

    context = {
        "books": books,
        "category": category_name
    }

    return render(request, "category.html", context)


def book_detail(request, id):

    book = get_object_or_404(Book, id=id)

    context = {
        'book': book
    }

    return render(request, 'book_detail.html', context)