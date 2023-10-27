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

from altar.forms.training import TrainingSessionExtrasForm, TrainingSessionForm

from altar.models.training import TrainingSession

# Create your views here.

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