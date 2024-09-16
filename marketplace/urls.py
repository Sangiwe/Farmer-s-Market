from django.urls import path
from . import views 
from .farmer_views import farmer_dashboard, manage_products, add_product, edit_product, delete_product, view_orders, analytics, account_settings
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
  path('', views.home, name='home'),
  path('dashboard/', views.dashboard_view, name='dashboard'),
  path('products/', views.product_list, name='product_list'),
  path('products/<int:pk>/', views.product_detail, name='product_detail'),
  path('products/<int:pk>/add_to_cart/', views.add_to_cart, name='add_to_cart'),
  path('products/<int:pk>/remove_from_cart/', views.remove_from_cart, name='remove_from_cart'),
  path('cart/', views.cart_contents, name='cart_contents'),
  path('checkout/', views.checkout, name='checkout'),
  path('thank_you/', views.thank_you, name='thank_you'),
    path('farmer-dashboard/', farmer_dashboard, name='farmer_dashboard'),
    path('manage-products/', manage_products, name='manage_products'),
    path('add-product/', add_product, name='add_product'),
    path('edit-product/<int:pk>/', edit_product, name='edit_product'),
    path('delete-product/<int:pk>/', delete_product, name='delete_product'),
    path('view-orders/', view_orders, name='view_orders'),
    path('analytics/', analytics, name='analytics'),
    path('account-settings/', account_settings, name='account_settings'),
    path('account-settings/change-password/', auth_views.PasswordChangeView.as_view(template_name='marketplace/farmer_dashboard/change_password.html'), name='change_password'),
    path('account-settings/change-password/done/', auth_views.PasswordChangeDoneView.as_view(template_name='marketplace/farmer_dashboard/change_password_done.html'), name='password_change_done'),
    path('place_order/', views.place_order, name='place_order'),
    path('order_confirmation/', views.order_confirmation, name='order_confirmation'),
    path('mark_order_completed/<int:order_id>/', views.mark_order_completed, name='mark_order_completed'),

] 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)