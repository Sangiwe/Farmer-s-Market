from django.contrib.auth import views as auth_views
from django.urls import path
from . import views
from marketplace import farmer_views, views as marketplace_views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('edit-profile/', views.edit_profile_view, name='edit_profile'),
    path('farmer-dashboard/', farmer_views.farmer_dashboard, name='farmer_dashboard'),
    path('dashboard/', marketplace_views.dashboard, name='dashboard'),
    path('farmer-dashboard/', farmer_views.farmer_dashboard, name='farmer_dashboard'),
    path('dashboard/', marketplace_views.dashboard, name='dashboard'),
]
