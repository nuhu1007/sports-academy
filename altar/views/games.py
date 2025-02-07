from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from altar.forms.games import GameExtrasForm, GameForm

from altar.models.games import Game

# Create your views here.
# Game Views
@login_required
def game_schedule(request):
    games = Game.objects.all()
    form = GameForm()

    # Scheduling the game
    if request.method == 'POST':
        form = GameForm(request.POST)
        if form.is_valid():
            game = form.save(commit=False)
            game.save()
            messages.success(request, f"Game scheduled and saved successfully")
            return redirect('game_schedule')
        else:
            form = GameForm()

    context = {
        'games': games,
        'form': GameForm()
    }
    return render(request, 'app/games/game_schedule.html', context)


@login_required
def game_details(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    form = GameExtrasForm(instance=game)

    # Add game results, comments & highlights
    if request.method == 'POST':
        form = GameExtrasForm(request.POST, request.FILES, instance=game)
        if form.is_valid():
            form.save()
            messages.success(request, f"Game updated successfully")
            return redirect('game_details', game_id=game.id)
        else:
            form = GameExtrasForm()

    context = {
        'game': game,
        'form': form,
    }
    return render(request, 'app/games/game_details.html', context)


@login_required
def match_results(request):
    games = Game.objects.all()

    context = {
        'games': games,
    }
    return render(request, 'app/games/match_results.html', context)