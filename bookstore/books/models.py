from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):

    CATEGORY_CHOICES = [
        ('fiction', 'Fiction'),
        ('mystery', 'Mystery'),
        ('scifi', 'Science Fiction'),
        ('romance', 'Romance'),
        ('biography', 'Biography'),
        ('selfhelp', 'Self Help'),
        ('business', 'Business'),
        ('history', 'History'),
    ]

    title = models.CharField(max_length=200)

    author = models.CharField(max_length=200)
    
    price = models.DecimalField(max_digits=6, decimal_places=2)
    
    image = models.ImageField(upload_to='book/')
    
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

    description = models.TextField()

    publisher = models.CharField(max_length=200)

    publication_date = models.DateField()

    isbn = models.CharField(max_length=20)

    pages = models.IntegerField()

    def __str__(self):
        return self.title


class Order(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.TextField()
    payment_method = models.CharField(max_length=50)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    quantity = models.IntegerField()