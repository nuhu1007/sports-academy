from django import forms

from altar.models.equipment import Equipments
from altar.models.branch import Branches

# Create here
class EquipmentForm(forms.ModelForm):
    equipment_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder':'Enter the equipment name', 'class':'form-control'}))
    equipment_number = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'placeholder': 'Enter the equipment number', 'class': 'form-control'}))
    equipment_branch = forms.ModelChoiceField(required=False, queryset=Branches.objects.all(), widget=forms.Select(attrs={'class':'my-select', 'placeholder':'Choose a branch...'}))

    class Meta:
        model = Equipments
        fields = ['equipment_name', 'equipment_number', 'equipment_branch']