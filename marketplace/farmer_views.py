from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Order, Farmer, OrderItem
from .forms import ProductForm
from django.db.models import Sum, Avg
from django.contrib.auth.forms import UserChangeForm
from .forms import CustomUserChangeForm
from django.contrib import messages

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

    context = {
        'total_sales': total_sales,
        'total_orders': total_orders,
        'avg_order_value': avg_order_value,
        'product_sales': product_sales,
        'best_selling_products': best_selling_products,
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










# # farmer_views.py
# from django.shortcuts import render, get_object_or_404, redirect
# from django.contrib.auth.decorators import login_required
# from .models import Product, Order, Farmer
# from .forms import ProductForm
# from django.db.models import Sum
# from django.contrib.auth.forms import UserChangeForm
# from .forms import CustomUserChangeForm
# from django.contrib import messages

# @login_required
# def farmer_dashboard(request):
#     try:
#         farmer = Farmer.objects.get(user=request.user)
#     except Farmer.DoesNotExist:
#         return render(request, 'marketplace/farmer_dashboard/no_profile.html')

#     products_count = Product.objects.filter(farmer=farmer).count()
#     orders_count = Order.objects.filter(product__farmer=farmer).count()
#     return render(request, 'marketplace/farmer_dashboard/dashboard_overview.html', {
#         'products_count': products_count,
#         'orders_count': orders_count,
#     })


# @login_required
# def manage_products(request):
#     user = request.user
#     products = Product.objects.filter(farmer=user.farmer)
#     return render(request, 'marketplace/farmer_dashboard/manage_products.html', {'products': products})

# @login_required
# def add_product(request):
#     if request.method == 'POST':
#         form = ProductForm(request.POST, request.FILES)
#         if form.is_valid():
#             product = form.save(commit=False)
#             product.farmer = request.user.farmer
#             product.save()
#             return redirect('manage_products')
#     else:
#         form = ProductForm()
#     return render(request, 'marketplace/farmer_dashboard/add_products.html', {'form': form})

# @login_required
# def edit_product(request, pk):
#     product = get_object_or_404(Product, pk=pk, farmer=request.user.farmer)
#     if request.method == 'POST':
#         form = ProductForm(request.POST, request.FILES, instance=product)
#         if form.is_valid():
#             form.save()
#             return redirect('manage_products')
#     else:
#         form = ProductForm(instance=product)
#     return render(request, 'marketplace/farmer_dashboard/edit_products.html', {'form': form})

# @login_required
# def delete_product(request, pk):
#     product = get_object_or_404(Product, pk=pk, farmer=request.user.farmer)
#     if request.method == 'POST':
#         product.delete()
#         return redirect('manage_products')
#     return render(request, 'marketplace/farmer_dashboard/confirm_delete.html', {'product': product})

# @login_required
# def view_orders(request):
#     user = request.user
#     orders = Order.objects.filter(product__farmer=user.farmer)
#     return render(request, 'marketplace/farmer_dashboard/view_orders.html', {'orders': orders})

# @login_required
# def analytics(request):
#     user = request.user
#     total_sales = Order.objects.filter(product__farmer=user.farmer).aggregate(Sum('quantity'))
#     return render(request, 'marketplace/farmer_dashboard/analytics.html', {
#         'total_sales': total_sales['quantity__sum'] or 0,
#     })

# def account_settings(request):
#     if request.method == 'POST':
#         form = CustomUserChangeForm(request.POST, instance=request.user)
#         if form.is_valid():
#             form.save()
#     else:
#         form = CustomUserChangeForm(instance=request.user)

#     return render(request, 'marketplace/farmer_dashboard/account_settings.html', {'form': form})

# @login_required
# def farmer_orders(request):
#     orders = Order.objects.all()  # You may want to filter orders specific to the farmer's products
#     return render(request, 'marketplace/dashboard_overview.html', {'orders': orders})

# @login_required
# def mark_order_completed(request, order_id):
#     order = Order.objects.get(id=order_id)
#     if request.method == 'POST':
#         order.status = 'Completed'
#         order.save()
#         messages.success(request, 'Order marked as completed.')
#     return redirect('farmer_orders')




