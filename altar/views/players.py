from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, logout as auth_logout, login as auth_login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.db.models import Count, OuterRef, Subquery, IntegerField
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone

from altar.forms.players import PlayerForm

from altar.models.branch import Branches
from altar.models.category import Categories
from altar.models.players import Player

# Create your views here.

# Players' Views
@login_required
def add_player(request):
    categories = Categories.objects.all()
    branches = Branches.objects.all()
    form = PlayerForm(request.POST, request.FILES)
    
    if request.method == 'POST':
        if form.is_valid():
            player = form.save(commit=False)
            player.save()
            messages.success(request, f"{player.full_name} has been registered and saved successfully.")
            return redirect('/players')
        else:
            form = PlayerForm()

    context = {
        'form': form,
        'categories': categories,
        'branches': branches,
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
    return render(request, 'app/players/player_details.html', context)