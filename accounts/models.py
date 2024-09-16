from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

# Create your models here.

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login after successful registration
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})
