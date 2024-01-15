from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from altar.models.branch import Branches
from altar.models.coaches import Coach
from altar.models.players import Player
from altar.models.training import TrainingSession
from altar.models.equipment import Equipments

# Create your views here.

def index(request):
    return render(request, 'index.html')


# Dashboard View
@login_required
def dashboard(request):
    coaches = Coach.objects.all()
    coach_count = len(coaches)

    players = Player.objects.all()
    player_count = len(players)

    branches = Branches.objects.all()
    branches_count = len(branches)

    sessions = TrainingSession.objects.all()
    sessions_count = len(sessions)

    equipments = Equipments.objects.all()
    equipment_count = len(equipments)

    context = {
        'coach_count': coach_count,
        'player_count': player_count,
        'players': players,
        'coaches': coaches,
        'branches_count': branches_count,
        'sessions_count': sessions_count,
        'equipment_count': equipment_count,
    }
    return render(request, 'app/dashboard.html', context)