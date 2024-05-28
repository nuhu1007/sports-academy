from django import forms
from django.contrib.auth.forms import UserCreationForm

from altar.models.user import User


# Create here
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


class LoginForm(forms.Form):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder':'Enter your email', 'class':'custom-email-input form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Enter your password', 'class':'prompt srch_explore form-control'}))

    # class Meta:
    #     model = User
    #     fields = ['email', 'password']