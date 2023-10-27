from django import forms

from altar.models.branch import Branches

# Create here
class BranchForm(forms.ModelForm):
    branch = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder':'Enter a branch e.g. Fedha, Baraka', 'class':'form-control'}))

    class Meta:
        model = Branches
        fields = ['branch',]