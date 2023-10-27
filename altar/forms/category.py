from django import forms

from altar.models.category import Categories

# Create here
class CategoryForm(forms.ModelForm):
    category = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder':'Enter a category e.g. Under 9s, Under 11s', 'class':'form-control'}))

    class Meta:
        model = Categories
        fields = ['category',]