from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, logout as auth_logout, login as auth_login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse
from django.utils import timezone

from altar.forms.training import AttendanceForm
from altar.models.players import Player
from altar.models.training import Attendance, TrainingSession

# Create your views here.
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