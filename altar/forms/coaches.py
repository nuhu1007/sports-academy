from django import forms

from altar.models.coaches import Coach
from altar.models.category import Categories
from altar.models.branch import Branches

# Create here
class CoachForm(forms.ModelForm):
    full_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder':'Full Name', 'class':'form-control'}))
    phone_number = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder':'Phone Number', 'class':'form-control'}))
    coaching_category = forms.ModelChoiceField(required=True, queryset=Categories.objects.all(), widget=forms.Select(attrs={'class':'form-control', 'placeholder':'Choose a category...'}))
    coaching_branch = forms.ModelChoiceField(required=True, queryset=Branches.objects.all(), widget=forms.Select(attrs={'class':'form-control', 'placeholder':'Choose a branch...'}))

    class Meta:
        model = Coach
        fields = ['full_name', 'phone_number', 'coaching_category', 'coaching_branch']