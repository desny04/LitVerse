from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('category/<str:category_name>/', views.category_books, name="category_books"),
    path('book/<int:id>/', views.book_detail, name='book_detail'),
]