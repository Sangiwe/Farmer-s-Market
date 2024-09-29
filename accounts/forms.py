from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

# Add a choice field for user type
USER_TYPE_CHOICES = (
    ('customer', 'Customer'),
    ('farmer', 'Farmer'),
)


# New registration form that includes user_type (farmer or customer)
class CustomUserRegistrationForm(UserCreationForm):
      USER_TYPE_CHOICES = [
        ('customer', 'Customer'),
        ('farmer', 'Farmer')
    ]
      
      user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES, required=True)

      class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'user_type']

# Existing form for updating user details
class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']  

   
    widgets = {
        'username': forms.TextInput(attrs={'class': 'form-control'}),
        'first_name': forms.TextInput(attrs={'class': 'form-control'}),
        'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        'email': forms.EmailInput(attrs={'class': 'form-control'}),
    }
