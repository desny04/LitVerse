from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Book

@login_required
def home(request):
    books = Book.objects.all()
    return render(request, 'home.html', {'books': books})
