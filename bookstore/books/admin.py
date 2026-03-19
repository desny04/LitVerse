from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Book)

from .models import Order, OrderItem

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'total', 'status', 'created_at']
    list_editable = ['status']   # 🔥 IMPORTANT (edit directly)

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)