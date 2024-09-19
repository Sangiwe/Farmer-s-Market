from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserRegistrationForm  # Import custom form
from django.contrib.auth.models import Group  # For assigning farmer/customer group
from .forms import CustomUserChangeForm



# Login View
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # Ensure the user has a profile (if not, create one)
            if not hasattr(user, 'profile'):
                Profile.objects.create(user=user, user_type='customer')  # Assuming default as 'customer'
            
            # Redirect based on user type (farmer or customer)
            if user.profile.user_type == 'farmer':
                return redirect('farmer_dashboard')  # Redirect to farmer dashboard
            else:
                return redirect('dashboard')  # Redirect to customer dashboard
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})



# Logout View
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to login after logout


# Registration View
from django.contrib.auth.models import Group
from .models import Profile  # Import Profile model

from django.db import IntegrityError

def register_view(request):
    if request.method == 'POST':
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                user_type = form.cleaned_data['user_type']
                Profile.objects.create(user=user, user_type=user_type)
                login(request, user)
                if user_type == 'farmer':
                    farmer_group, created = Group.objects.get_or_create(name='Farmer')
                    user.groups.add(farmer_group)
                    return redirect('farmer_dashboard')
                else:
                    customer_group, created = Group.objects.get_or_create(name='Customer')
                    user.groups.add(customer_group)
                    return redirect('dashboard')
            except IntegrityError as e:
                print(f'IntegrityError: {e}')
                # Optionally, you can add a message for the user here
        else:
            # Handle form errors
            print(form.errors)
    else:
        form = CustomUserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})


# def register_view(request):
#     if request.method == 'POST':
#         form = CustomUserRegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save()  # Save the user
#             user_type = form.cleaned_data['user_type']

#             # Create a Profile instance and assign the user_type
#             Profile.objects.create(user=user, user_type=user_type)

#             login(request, user)  # Log the user in

#             # Assign the user to a group based on their selection (farmer/customer)
#             if user_type == 'farmer':
#                 farmer_group, created = Group.objects.get_or_create(name='Farmer')
#                 user.groups.add(farmer_group)
#                 return redirect('farmer_dashboard')  # Redirect farmer to farmer dashboard
#             else:
#                 customer_group, created = Group.objects.get_or_create(name='Customer')
#                 user.groups.add(customer_group)
#                 return redirect('dashboard')  # Redirect customer to customer dashboard
#     else:
#         form = CustomUserRegistrationForm()

#     return render(request, 'accounts/register.html', {'form': form})



@login_required
def edit_profile_view(request):
    user = request.user
    
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  # Redirect to a common dashboard or specific dashboard
    else:
        form = CustomUserChangeForm(instance=user)
    
    return render(request, 'accounts/edit_profile.html', {'form': form})


