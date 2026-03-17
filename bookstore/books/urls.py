from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('category/<str:category_name>/', views.category_books, name="category_books"),
    path('book/<int:id>/', views.book_detail, name='book_detail'),
    path("cart/", views.cart, name="cart"),
    path('add-to-cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:id>/', views.remove_from_cart, name='remove_from_cart'),
    path("update-cart/<int:id>/<str:action>/", views.update_cart, name="update_cart"),
    path("wishlist/", views.wishlist, name="wishlist"),
    path('toggle-wishlist/<int:id>/', views.toggle_wishlist, name='toggle_wishlist'),
    path('remove-from-wishlist/<int:id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
]