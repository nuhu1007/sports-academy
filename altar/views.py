from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.db.models import Count

import pdfkit

from . models import Categories, Player
from .forms import LoginForm, CategoryForm, PlayerForm

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
        return render(request, 'authentication/login.html', {'form':LoginForm()})


class ResetPasswordView(PasswordResetView, SuccessMessageMixin):
    template_name = 'authentication/password-reset.html'
    email_template_name = 'authentication/password-reset-email.html'
    subject_template_name = 'authentication/password-reset-subject.txt'
    success_message = "We have sent you an email with instructions for changing your password." \
                      "If an account exists with the email you entered, you should receive them shortly." \
                      "If you don't receive an email, " \
                      "please make sure you entered the address you registered with and check your spam folder."
    success_url = reverse_lazy("verification")


class VerificationEmail(TemplateView):
    template_name ="authentication/verification-email-sent.html"
    

def index(request):
    return render(request, 'index.html')


@login_required
def dashboard(request):
    under_9 = get_object_or_404(Categories, id=1)
    under9_count = Player.objects.filter(player_category=under_9).count()
    under_11 = get_object_or_404(Categories, id=2)
    under11_count = Player.objects.filter(player_category=under_11).count()
    under_13 = get_object_or_404(Categories, id=3)
    under13_count = Player.objects.filter(player_category=under_13).count()

    context = {
        'under9_count': under9_count,
        'under11_count': under11_count,
        'under13_count': under13_count,
    }
    return render(request, 'app/dashboard.html', context)


# Category View
@login_required
def categories(request):
    categories = Categories.objects.annotate(player_count=Count('player_category'))
    form = CategoryForm()

    # Creating a category
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.save()
            messages.success(request, f"Category added and saved successfully.")
            return redirect('categories')
        else:
            form = CategoryForm()

    context = {
        'categories': categories,
        'form': CategoryForm(),
    }
    return render(request, 'app/categories.html', context)


# Players' View
@login_required
def add_player(request):
    categories = Categories.objects.all()
    form = PlayerForm(request.POST)
    
    if request.method == 'POST':
        if form.is_valid():
            player = form.save(commit=False)
            player.save()
            messages.success(request, f"{player.full_name} has been created and saved successfully.")
            return redirect('/players')
        else:
            form = PlayerForm()

    context = {
        'form': form,
        'categories': categories,
    }
    return render(request, 'app/players/add_player.html', context)


@login_required
def players_list(request):
    players = Player.objects.all()

    context = {
        'players': players,
    }
    return render(request, 'app/players/players_list.html', context)


@login_required
def player_details(request, player_id):
    player = get_object_or_404(Player, id=player_id)

    context = {
        'player': player
    }

    if request.method == 'POST':
        # Generate PDF
        html_string = render_to_string('app/players/player_details.html', context)

        options = {
            'page-size': 'A4',
            'encoding': 'UTF-8',
        }
        
        pdf = pdfkit.from_string(html_string, False, options)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="player_details.pdf"'
        response.write(pdf)
        return response

    return render(request, 'app/players/player_details.html', context)


# Training Views
@login_required
def training_management(request):
    return render(request, 'app/training/training_management.html')