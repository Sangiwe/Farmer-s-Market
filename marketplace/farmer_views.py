from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Order, Farmer, OrderItem
from .forms import ProductForm
from django.db.models import Sum, Avg
from django.contrib.auth.forms import UserChangeForm
from accounts.forms import CustomUserChangeForm
from django.contrib import messages
import json

@login_required
def farmer_dashboard(request):
    try:
        farmer = Farmer.objects.get(user=request.user)
    except Farmer.DoesNotExist:
        return render(request, 'marketplace/farmer_dashboard/no_profile.html')

    products_count = Product.objects.filter(farmer=farmer).count()
    orders_count = OrderItem.objects.filter(product__farmer=farmer).count()
    orders = Order.objects.filter(orderitem__product__farmer=farmer).distinct()  # Fetch orders for the farmer

    return render(request, 'marketplace/farmer_dashboard/dashboard_overview.html', {
        'products_count': products_count,
        'orders_count': orders_count,
        'orders': orders,  # Pass orders to the template
    })


@login_required
def manage_products(request):
    user = request.user
    products = Product.objects.filter(farmer=user.farmer)
    return render(request, 'marketplace/farmer_dashboard/manage_products.html', {'products': products})

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.farmer = request.user.farmer
            product.save()
            return redirect('manage_products')
    else:
        form = ProductForm()
    return render(request, 'marketplace/farmer_dashboard/add_products.html', {'form': form})

@login_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk, farmer=request.user.farmer)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('manage_products')
    else:
        form = ProductForm(instance=product)
    return render(request, 'marketplace/farmer_dashboard/edit_products.html', {'form': form})

@login_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk, farmer=request.user.farmer)
    if request.method == 'POST':
        product.delete()
        return redirect('manage_products')
    return render(request, 'marketplace/farmer_dashboard/confirm_delete.html', {'product': product})

@login_required
def view_orders(request):
    try:
        farmer = Farmer.objects.get(user=request.user)
    except Farmer.DoesNotExist:
        return render(request, 'marketplace/farmer_dashboard/no_profile.html')

    # Get orders directly where the farmer's products are included
    orders = Order.objects.filter(orderitem__product__farmer=farmer).distinct()

    return render(request, 'marketplace/farmer_dashboard/view_orders.html', {
        'orders': orders,
    })


@login_required
def analytics(request):
    # Ensure the logged-in user is a farmer
    try:
        farmer = Farmer.objects.get(user=request.user)
    except Farmer.DoesNotExist:
        return render(request, 'marketplace/farmer_dashboard/no_profile.html')

    # Total Sales for all products of this farmer
    total_sales = Order.objects.filter(orderitem__product__farmer=farmer, status='Completed')\
                               .aggregate(total_sales=Sum('total_amount'))['total_sales'] or 0

    # Total Orders for the farmer's products
    total_orders = Order.objects.filter(orderitem__product__farmer=farmer, status='Completed').count()

    # Average Order Value
    avg_order_value = Order.objects.filter(orderitem__product__farmer=farmer, status='Completed')\
                                   .aggregate(avg_value=Avg('total_amount'))['avg_value'] or 0

    # Sales by Product (units sold)
    product_sales = Product.objects.filter(farmer=farmer)\
                                   .annotate(total_sold=Sum('orderitem__quantity'))\
                                   .order_by('-total_sold')

    # Best-selling products
    best_selling_products = product_sales[:5]  # Top 5 best-selling products

    # Extract product names and units sold for Chart.js
    product_names = [product.name for product in product_sales]
    product_sold_data = [product.total_sold or 0 for product in product_sales]

    # Pass the data to the template as JSON
    context = {
        'total_sales': total_sales,
        'total_orders': total_orders,
        'avg_order_value': round(avg_order_value, 2),
        'product_sales': product_sales,
        'best_selling_products': best_selling_products,
        'chart_labels': json.dumps(product_names),  # JSON-encoded labels for Chart.js
        'chart_data': json.dumps(product_sold_data),  # JSON-encoded data for Chart.js
    }

    return render(request, 'marketplace/farmer_dashboard/analytics.html', context)

@login_required
def account_settings(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account settings have been updated.')
    else:
        form = CustomUserChangeForm(instance=request.user)

    return render(request, 'marketplace/farmer_dashboard/account_settings.html', {'form': form})









