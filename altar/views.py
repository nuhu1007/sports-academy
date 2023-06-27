from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import LoginForm

# Create your views here.

# Authentication Views
def login(request):
    if request.method == 'POST':
        user = authenticate(request, email=request.POST['email'], password=request.POST['password'])
        if user:
            auth_login(request, user)
            messages.success(request, f'Successfully logged in')
            return redirect('dashboard')
        else:
            messages.error(request, f'Incorrect credentials.')
            return render(request, 'authentication/login.html', {'form':LoginForm()})
    else:
        messages.error(request, f'Check your details and try again.')
        return render(request, 'authentication/login.html', {'form':LoginForm()})
    


def index(request):
    return render(request, 'index.html')


@login_required
def dashboard(request):
    return render(request, 'app/dashboard.html')