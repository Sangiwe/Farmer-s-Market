from django.contrib import admin
from .models import Product, Farmer, Order, Cart, CartItem, Category, OrderItem

from django.contrib import admin
from .models import Product, Farmer, Order, Cart, CartItem, Category

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category')
    search_fields = ('name',)

@admin.register(Farmer)
class FarmerAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'contact_number', 'email', 'description', 'registered_on')

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'total_amount', 'status', 'order_date')
    inlines = [OrderItemInline]

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


# # Register your models here.
# admin.site.register(Product)
# admin.site.register(Farmer)
# admin.site.register(Order)
# admin.site.register(Cart)
# admin.site.register(CartItem)
# admin.site.register(Category)


