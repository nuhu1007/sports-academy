from django import forms
from django.contrib import messages

from altar.models.branch import Branches
from altar.models.players import Player
from altar.models.training import Attendance, TrainingSession

# Create here
class TrainingSessionForm(forms.ModelForm):
    training_branch = forms.ModelChoiceField(required=True, queryset=Branches.objects.all(), widget=forms.Select(attrs={'class':'form-control', 'placeholder':'Select a branch...'}))
    date = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date', 'placeholder':'Enter the date', 'class':'form-control'}))
    start_time = forms.TimeField(required=True, widget=forms.TimeInput(attrs={'type':'time', 'placeholder':'Enter the time', 'class':'form-control'}))
    end_time = forms.TimeField(required=True, widget=forms.TimeInput(attrs={'type':'time', 'placeholder':'Enter the time', 'class':'form-control'}))
    location = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder':'Enter the location', 'class':'form-control'}))

    class Meta:
        model = TrainingSession
        fields = ['training_branch' ,'date', 'start_time', 'end_time', 'location']


class TrainingSessionExtrasForm(forms.ModelForm):
    notes = forms.CharField(required=False, widget=forms.Textarea(attrs={'placeholder':'Any notes about the training session', 'class':'form-control'}))
    highlights = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={'class':'form-control'}))

    class Meta:
        model = TrainingSession
        fields = ['notes', 'highlights']



class AttendanceForm(forms.Form):
    def __init__(self, *args, **kwargs):
        training_session = kwargs.pop('training_session')
        super().__init__(*args, **kwargs)

        # Retrieve the branch associated with the training session
        branch = training_session.training_branch

        # Filter the players based on the selected branch
        players = Player.objects.filter(player_branch=branch)

        for player in players:
            self.fields[f'player_{player.id}'] = forms.BooleanField(label=player.full_name, required=False)

    def save(self, training_session):
        attendance_exists = Attendance.objects.filter(training_session=training_session).exists()
        if not attendance_exists:
            for name, value in self.cleaned_data.items():
                if value:
                    player_id = int(name.split('_')[1])
                    player = Player.objects.get(id=player_id)
                    attendance, created = Attendance.objects.get_or_create(
                        player=player,
                        training_session=training_session,
                    )
                    if not attendance.attended:
                        attendance.attended = True
                        attendance.save()
                        messages.success(
                            self.request,
                            f"Attendance marked for {player.full_name}."
                        )
                    else:
                        messages.warning(
                            self.request,
                            f"Attendance already marked for {player.full_name}."
                        )
                else:
                    player_id = int(name.split('_')[1])
                    player = Player.objects.get(id=player_id)
                    attendance = Attendance.objects.filter(
                        player=player,
                        training_session=training_session,
                    ).first()
                    if attendance:
                        attendance.delete()
                        messages.success(
                            self.request,
                            f"Attendance deleted for {player.full_name}."
                        )