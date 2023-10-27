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

from altar.forms.equipment import EquipmentForm

from altar.models.equipment import Equipments

# Create your views here.

# Equipments View
@login_required
def equipments(request):
    equipments = Equipments.objects.all()
    form = EquipmentForm()

    # Creating or Editing a new Equipment
    if request.method == 'POST':
        if 'add_equipment' in request.POST: # Check if form is for adding an equipment
            form = EquipmentForm(request.POST)
            if form.is_valid():
                equipment = form.save(commit=False)
                equipment.save()
                messages.success(request, f"{equipment.equipment_name} added and saved successfully.")
                return redirect ('equipments')
            else:
                messages.error(request, f"Failed to add.")
                form = EquipmentForm()

        elif 'edit_equipment' in request.POST: #Check if the form is for editing an equipment
            equipment_id = request.POST.get('equipment_id')
            equipment = get_object_or_404(Equipments, pk=equipment_id)
            edit_form = EquipmentForm(request.POST, instance=equipment)
            if edit_form.is_valid():
                edit_form.save()
                messages.success(request, f"Equipment edited and saved successfully.")
                return redirect('equipments')
            else:
                messages.error(request, f"Failed to edit.")
                edit_form = EquipmentForm(instance=equipment)

    context = {
        'equipments': equipments,
        'form': form,
    }
    return render(request, 'app/equipments.html', context)


@require_POST
@login_required
def delete_equipment(request, equipment_id):
    equipment = get_object_or_404(Equipments, pk=equipment_id)
    equipment.delete()
    return JsonResponse({'message': 'Equipment deleted successfully.'})