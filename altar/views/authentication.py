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