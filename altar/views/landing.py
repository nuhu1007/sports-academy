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

from altar.models import Categories, Player, TrainingSession, Attendance, Game, Coach, Branches, Equipments
from altar.forms import LoginForm, CategoryForm, PlayerForm, TrainingSessionForm, AttendanceForm, TrainingSessionExtrasForm, GameForm, GameExtrasForm, CoachForm, BranchForm, EquipmentForm

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

    context = {
        'coach_count': coach_count,
        'player_count': player_count,
        'players': players,
        'coaches': coaches,
        'branches_count': branches_count,
        'sessions_count': sessions_count,
    }
    return render(request, 'app/dashboard.html', context)