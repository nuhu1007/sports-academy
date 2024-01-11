from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from altar.forms.players import PlayerForm
from altar.models.branch import Branches
from altar.models.category import Categories
from altar.models.players import Player

# Create your views here.

# Players' Views
@login_required
def add_player(request):
    form = PlayerForm(request.POST, request.FILES)
    
    if request.method == 'POST':
        if form.is_valid():
            player = form.save(commit=False)
            player.save()
            messages.success(request, f"{player.full_name} has been registered and saved successfully.")
            return redirect('players')
        else:
            form = PlayerForm()

    context = {
        'form': form,
        'categories': Categories.objects.all(),
        'branches': Branches.objects.all(),
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


class EditPlayer(LoginRequiredMixin, View):
    template_name = 'app/players/edit_player.html'

    def get(self, request, player_id):
        player = get_object_or_404(Player, id=player_id)
        form = PlayerForm(instance=player)

        context = {
            'player': player,
            'form': form
        }
        return render(request, self.template_name, context)

    def post(self, request, player_id):
        player = get_object_or_404(Player, id=player_id)
        form = PlayerForm(request.POST, instance=player)
        if form.is_valid():
            form.save()
            messages.success(request, f"Player details edited successfully.")
            return redirect('players')
        else:
            messages.warning(request, f"{form.errors}")
            form = PlayerForm(instance=player)

        context = {
            'form': form,
        }
        return render(request, self.template_name, context)