from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

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

class EquipmentsView(LoginRequiredMixin, View):
    template_name = 'app/equipments.html'

    def get(self, request):

        context = {
            'form': EquipmentForm(),
            'equipments': Equipments.objects.all()
        }
        return render(request, self.template_name, context)


class DeleteEquipment(LoginRequiredMixin, View):
    def post(self, request, equipment_id):
        equipment = get_object_or_404(Equipments, id=equipment_id)
        equipment.delete()
        messages.info(request, f"Equipment deleted successfully")
        return redirect('equipments')