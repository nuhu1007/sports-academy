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

from . models import Categories, Player, TrainingSession, Attendance, Game, Coach, Branches
from .forms import LoginForm, CategoryForm, PlayerForm, TrainingSessionForm, AttendanceForm, TrainingSessionExtrasForm, GameForm, GameExtrasForm, CoachForm, BranchForm

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
    

@login_required
def logout(request):
    auth_logout(request)
    messages.success(request, f"Successfully logged out")
    return redirect('login')


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

@require_POST
@login_required
def delete_category(request, category_id):
    category = get_object_or_404(Categories, pk=category_id)
    category.delete()
    return JsonResponse({'message': 'Category deleted successfully.'})


# Branch View
@login_required
def branches(request):
    # Subquery to get the player count & coach count for each branch
    player_count_subquery = Player.objects.filter(player_branch=OuterRef('pk')).values('player_branch').annotate(count=Count('*')).values('count')
    coach_count_subquery = Coach.objects.filter(coaching_branch=OuterRef('pk')).values('coaching_branch').annotate(count=Count('*')).values('count')
    branches = Branches.objects.annotate(player_count=Subquery(player_count_subquery, output_field=IntegerField()), coach_count=Subquery(coach_count_subquery, output_field=IntegerField()))
    form = BranchForm()

    # Creating a branch
    if request.method == 'POST':
        form = BranchForm(request.POST)
        if form.is_valid():
            branch = form.save(commit=False)
            branch.save()
            messages.success(request, f"Branch added and saved successfully.")
            return redirect('branches')
        else:
            form = BranchForm()

    context = {
        'branches': branches,
        'form': BranchForm(),
    }
    return render(request, 'app/branches.html', context)


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


# Training Views
@login_required
def training_management(request):
    trainings = TrainingSession.objects.all()
    form = TrainingSessionForm()

    # Creating the training schedule
    if request.method == 'POST':
        form = TrainingSessionForm(request.POST)
        if form.is_valid():
            training = form.save(commit=False)
            training.save()
            messages.success(request, f"Training schedule created and saved successfully.")
            return redirect('training_management')
        else:
            form = TrainingSessionForm()

    context = {
        'trainings': trainings,
        'form': TrainingSessionForm()
    }
    return render(request, 'app/training/training_management.html', context)


@login_required
def training_details(request, training_id):
    training = get_object_or_404(TrainingSession, id=training_id)
    form = TrainingSessionExtrasForm(instance=training)

    # Adding training notes & highlights
    if request.method == 'POST':
        form = TrainingSessionExtrasForm(request.POST, request.FILES, instance=training)
        if form.is_valid():
            form.save()
            messages.success(request, f"Training session has been updated successfully.")
            return redirect('training_details', training_id=training.id)
        else:
            form = TrainingSessionExtrasForm()

    context = {
        'training': training,
        'form': form
    }
    return render(request, 'app/training/training_details.html', context)


# Attendance Views
@login_required
def attendance_management(request):
    sessions = TrainingSession.objects.all()

    context = {
        'sessions': sessions,
    }
    return render(request, 'app/attendance/attendance_management.html', context)


@login_required
def record_attendance(request, session_id):
    session = get_object_or_404(TrainingSession, pk=session_id)
    ballers = session.players.all()

    # Retrieve the branch associated with the training session
    branch = session.training_branch

    # Filter players based on the branch
    players = Player.objects.filter(player_branch=branch)

    attendance_records = {}
    for player in players:
        attendance = Attendance.objects.filter(player=player, training_session=session).first()
        attendance_records[player] = attendance

    # Marking the attendance
    if request.method == 'POST':
        form = AttendanceForm(request.POST, training_session=session)
        if form.is_valid():
            form.request = request
            form.save(session)
            messages.success(request, f"Attendance marked and saved successfully.")
            return redirect('record_attendance', session_id=session.id)
    else:
        form = AttendanceForm(training_session=session)

    context = {
        'session': session,
        'players': players,
        'ballers': ballers,
        'attendance_records': attendance_records,
        'form': form,
    }
    return render(request, 'app/attendance/attendance_details.html', context)


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


# Coaches' Views
@login_required
def coaches_list(request):
    coaches = Coach.objects.all()
    form = CoachForm()

    # Registering a coach
    if request.method == 'POST':
        form = CoachForm(request.POST, request.FILES)
        if form.is_valid():
            coach = form.save(commit=False)
            coach.save()
            messages.success(request, f"{coach.full_name} registered and saved successfully.")
            return redirect('coaches')
        else:
            form = CoachForm()

    context = {
        'coaches': coaches,
        'form': CoachForm()
    }
    return render(request, 'app/coaches/coaches_list.html', context)