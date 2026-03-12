from django.shortcuts import render,redirect, get_object_or_404
from django.db.models import Q
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


from django.http import JsonResponse
from .models import Book

def add_to_cart(request, id):

    cart = request.session.get('cart', {})

    if str(id) in cart:
        cart[str(id)] += 1
    else:
        cart[str(id)] = 1

    request.session['cart'] = cart

    cart_count = sum(cart.values())

    return JsonResponse({'cart_count': cart_count})


# 

def cart(request):

    cart = request.session.get('cart', {})

    books = Book.objects.filter(id__in=cart.keys())

    cart_items = []

    for book in books:
        cart_items.append({
            'book': book,
            'quantity': cart[str(book.id)]
        })

    context = {
        'cart_items': cart_items
    }

    return render(request, "cart.html", context)


def remove_from_cart(request, id):

    cart = request.session.get('cart', {})

    if str(id) in cart:
        del cart[str(id)]

    request.session['cart'] = cart

    return redirect('cart')