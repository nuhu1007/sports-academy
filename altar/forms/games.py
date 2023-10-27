from django import forms

from altar.models.games import Game
from altar.models.players import Player

# Create here
class GameForm(forms.ModelForm):
    opponent = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder':'Opponent', 'class':'form-control'}))
    date = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date', 'placeholder':'Enter the date', 'class':'form-control'}))
    time = forms.TimeField(required=True, widget=forms.TimeInput(attrs={'type':'time', 'placeholder':'Enter the time', 'class':'form-control'}))
    location = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder':'Enter the location', 'class':'form-control'}))

    class Meta:
        model = Game
        fields = ['opponent', 'date', 'time', 'location']


class GameExtrasForm(forms.ModelForm):
    result = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'placeholder':'Game Result', 'class':'form-control'}))
    scorers = forms.ModelMultipleChoiceField(queryset=Player.objects.all(), required=False, widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}))
    comments = forms.CharField(required=False, widget=forms.Textarea(attrs={'placeholder':'Any comments about the game...', 'class':'form-control'}))
    highlights = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={'class':'form-control'}))

    class Meta:
        model = Game
        fields = ['result', 'scorers', 'comments', 'highlights']