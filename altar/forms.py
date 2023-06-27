from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User

# Create Here
class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'prompt srch_explore'}))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'prompt srch_explore'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'custom-email-input'}))
    phone_number = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Phone Number', 'class': 'prompt srch_explore'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password', 'class': 'prompt srch_explore'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class': 'prompt srch_explore'}))
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email', 'phone_number')


class LoginForm(forms.ModelForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'custom-email-input'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password', 'class': 'prompt srch_explore'}))

    class Meta:
        model = User
        fields = ['email', 'password']