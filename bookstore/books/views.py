from django.shortcuts import render,redirect, get_object_or_404
from django.db.models import Q
from django.http import JsonResponse
from decimal import Decimal
from .models import Book
from .models import Order, OrderItem
from django.core.mail import send_mail
from django.conf import settings


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

def cart(request):

    cart = request.session.get("cart", {})

    books = Book.objects.filter(id__in=cart.keys())

    cart_items = []

    for book in books:
        cart_items.append({
            "book": book,
            "quantity": cart[str(book.id)],
            "item_total": book.price * cart[str(book.id)]
        })

    context = {
        "cart_items": cart_items
    }

    return render(request, "cart.html", context)



def add_to_cart(request, id):

    cart = request.session.get('cart', {})
    id = str(id)

    if id in cart:
        cart[id] += 1
    else:
        cart[id] = 1

    request.session['cart'] = cart

    cart_count = sum(cart.values())

    return JsonResponse({'cart_count': cart_count})

def cart(request):

    cart = request.session.get("cart", {})

    books = Book.objects.filter(id__in=cart.keys())

    cart_items = []
    subtotal = Decimal('0.00')

    for book in books:
        qty = cart[str(book.id)]
        item_total = book.price * qty
        subtotal += item_total

        cart_items.append({
            "book": book,
            "quantity": qty,
            "item_total": item_total
        })

    shipping = Decimal('0.00')
    tax = subtotal * Decimal('0.10')
    total = subtotal + tax + shipping

    context = {
        "cart_items": cart_items,
        "subtotal": subtotal,
        "shipping": shipping,
        "tax": tax,
        "total": total
    }

    return render(request, "cart.html", context)


def remove_from_cart(request, id):

    cart = request.session.get('cart', {})

    if str(id) in cart:
        del cart[str(id)]

    request.session['cart'] = cart

    return redirect('cart')



def update_cart(request, id, action):

    cart = request.session.get('cart', {})
    id = str(id)

    if id in cart:

        if action == "increase":
            cart[id] += 1

        elif action == "decrease":
            cart[id] -= 1

            if cart[id] <= 0:
                del cart[id]

    request.session["cart"] = cart

    return redirect("cart")


def toggle_wishlist(request, id):

    wishlist = request.session.get('wishlist', [])

    id = str(id)   
    if id in wishlist:
        wishlist.remove(id)
        in_wishlist = False
    else:
        wishlist.append(id)
        in_wishlist = True

    request.session['wishlist'] = wishlist

    return JsonResponse({'in_wishlist': in_wishlist})


def wishlist(request):

    wishlist = request.session.get('wishlist', [])

    books = Book.objects.filter(id__in=wishlist)

    return render(request, 'wishlist.html', {'books': books})

def remove_from_wishlist(request, id):

    wishlist = request.session.get('wishlist', [])

    id = str(id)

    if id in wishlist:
        wishlist.remove(id)

    request.session['wishlist'] = wishlist

    return redirect('wishlist')





def checkout(request):

    cart = request.session.get('cart', {})

    if request.method == "POST":

        name = request.POST.get("name")
        email = request.POST.get("email")
        address = request.POST.get("address")
        payment = request.POST.get("payment")

        total = 0

        send_mail(
            subject="Order Placed - LitVerse",
            message = f"""
                    Hi {name},
                    Your order has been placed successfully 🎉
                    Thank you for shopping with LitVerse 📚
                    """,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False,
        )

        # create order
        order = Order.objects.create(
            user=request.user,
            name=name,
            email=email,
            address=address,
            payment_method=payment,
            total=0
        )

        for book_id, quantity in cart.items():
            book = Book.objects.get(id=book_id)
            item_total = book.price * quantity
            total += item_total

            OrderItem.objects.create(
                order=order,
                book=book,
                quantity=quantity
            )

        order.total = total
        order.save()

        # ✅ CLEAR CART
        request.session['cart'] = {}

        return redirect('success')

    return render(request, "checkout.html")



def success(request):
    return render(request, "success.html")


def my_orders(request):

    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    return render(request, "my_orders.html", {
        'orders': orders
    })




def cancel_order(request, order_id):
    order = Order.objects.get(id=order_id, user=request.user)

    if order.status == 'pending':
        order.status = 'cancelled'
        order.save()

    return redirect('my_orders')