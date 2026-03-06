from django.shortcuts import render
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