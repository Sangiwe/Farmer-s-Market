from django.shortcuts import render
from .models import Product, Category, Order, OrderItem
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem
from django.contrib import messages

# Create your views here.
def home(request):
    return render(request, 'marketplace/home.html')

def product_list(request):
    search_query = request.GET.get('search', '')
    category_filter = request.GET.get('category', '')
    price_range = request.GET.get('price_range', '')
    
    # Get all products and filter by search query
    products = Product.objects.filter(name__icontains=search_query)
    categories = Category.objects.all()

    # Apply Category Filter
    if category_filter:
        products = products.filter(category__id=category_filter)

    # Apply Price Range Filter
    if price_range:
        low, high = map(int, price_range.split('-'))
        products = products.filter(price__gte=low, price__lte=high)

    return render(request, 'marketplace/product_list.html', {
        'products': products,
        'categories': categories
    })

@login_required
def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item = CartItem.objects.filter(cart=cart, product=product).first()

    recommended_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]

    return render(request, 'marketplace/product_detail.html', {
        'product': product,
        'cart_item': cart_item,
        'quantity_range': range(1, 11),  # Adjust range if needed
        'recommended_products': recommended_products
    })

@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    quantity = int(request.POST.get('quantity', 1))  # Get the quantity from the form, default to 1 if not provided
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    if created:
        # If the item is added to the cart for the first time
        cart_item.quantity = quantity
    else:
        # If the item already exists in the cart, add the new quantity
        cart_item.quantity += quantity
    
    cart_item.save()
    messages.success(request, f'Added {quantity} {product.name} to your cart.')
    return redirect('product_detail', pk=pk)



@login_required
def remove_from_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart = Cart.objects.get(user=request.user)
    cart_item = CartItem.objects.filter(cart=cart, product=product).first()
    if cart_item:
        cart_item.delete()
        messages.success(request, f'Removed {product.name} from your cart.')
    else:
        messages.error(request, f'Item {product.name} not found in your cart.')
    return redirect('cart_contents')

from django.contrib.auth.decorators import login_required


@login_required
def cart_contents(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)

    # Calculate the total amount
    total_amount = sum(item.quantity * item.product.price for item in cart_items)

    return render(request, 'marketplace/cart_contents.html', {
        'cart_items': cart_items,
        'total_amount': total_amount,
    })


@login_required
def checkout(request):
    if request.method == 'POST':
        # Implement checkout logic here (e.g., processing payment, saving order, etc.)
        
        # On success, redirect to thank you page
        return redirect('thank_you')
    else:
        # If not POST request, render checkout page
        return render(request, 'marketplace/checkout.html')
    
def thank_you(request):
    return render(request, 'marketplace/thank_you.html')



@login_required
def dashboard (request):
    return render(request, 'marketplace/dashboard.html')

@login_required
def place_order(request):
    # Get or create a cart for the logged-in user
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    
    if cart_items:
        # Calculate total amount
        total_amount = sum(item.product.price * item.quantity for item in cart_items)

        # Create order
        order = Order.objects.create(customer=request.user, total_amount=total_amount)

        # Create order items and associate them with the order
        for item in cart_items:
            OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)

        # Clear the user's cart after placing the order
        cart_items.delete()

        messages.success(request, "Your order has been placed successfully!")

    return redirect('order_confirmation')


def order_confirmation(request):
    return render(request, 'marketplace/order_confirmation.html')

@login_required
def mark_order_completed(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        order.status = 'Completed'
        order.save()
        messages.success(request, 'Order marked as completed.')
    return redirect('view_orders')  # Or any appropriate view

# Placeholder views for About Us, Contact, and Privacy Policy
def about_us_view(request):
    return render(request, 'marketplace/about_us.html')

def contact_view(request):
    return render(request, 'marketplace/contact.html')

def privacy_policy_view(request):
    return render(request, 'marketplace/privacy_policy.html')
