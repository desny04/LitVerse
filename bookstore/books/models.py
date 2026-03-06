from django.db import models

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

    def __str__(self):
        return self.title