from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from .models import User, Categories, Player, TrainingSession, Attendance, Game, Coach, Branches

# Create Here
class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'prompt srch_explore'}))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'prompt srch_explore'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'custom-email-input'}))
    phone_number = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Phone Number', 'class': 'prompt srch_explore'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password', 'class': 'prompt srch_explore'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class': 'prompt srch_explore'}))
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email', 'phone_number')


class LoginForm(forms.ModelForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder':'Enter your email', 'class':'custom-email-input form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Enter your password', 'class':'prompt srch_explore form-control'}))

    class Meta:
        model = User
        fields = ['email', 'password']


class CategoryForm(forms.ModelForm):
    category = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder':'Enter a category e.g. Under 9s, Under 11s', 'class':'form-control'}))

    class Meta:
        model = Categories
        fields = ['category',]


class BranchForm(forms.ModelForm):
    branch = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder':'Enter a branch e.g. Fedha, Baraka', 'class':'form-control'}))

    class Meta:
        model = Branches
        fields = ['branch',]


class TrainingSessionForm(forms.ModelForm):
    date = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date', 'placeholder':'Enter the date', 'class':'form-control'}))
    start_time = forms.TimeField(required=True, widget=forms.TimeInput(attrs={'type':'time', 'placeholder':'Enter the time', 'class':'form-control'}))
    end_time = forms.TimeField(required=True, widget=forms.TimeInput(attrs={'type':'time', 'placeholder':'Enter the time', 'class':'form-control'}))
    location = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder':'Enter the location', 'class':'form-control'}))

    class Meta:
        model = TrainingSession
        fields = ['date', 'start_time', 'end_time', 'location']


class TrainingSessionExtrasForm(forms.ModelForm):
    notes = forms.CharField(required=False, widget=forms.Textarea(attrs={'placeholder':'Any notes about the training session', 'class':'form-control'}))
    highlights = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={'class':'form-control'}))

    class Meta:
        model = TrainingSession
        fields = ['notes', 'highlights']


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
    comments = forms.CharField(required=False, widget=forms.Textarea(attrs={'placeholder':'Any comments about the game...', 'class':'form-control'}))
    highlights = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={'class':'form-control'}))

    class Meta:
        model = Game
        fields = ['result', 'comments', 'highlights']


class CoachForm(forms.ModelForm):
    full_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder':'Full Name', 'class':'form-control'}))
    phone_number = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder':'Phone Number', 'class':'form-control'}))
    coach_image = forms.ImageField(required=True, widget=forms.ClearableFileInput(attrs={'class':'custom-image-field'}))
    coaching_category = forms.ModelChoiceField(required=True, queryset=Categories.objects.all(), widget=forms.Select(attrs={'class':'my-select', 'placeholder':'Choose a category...'}))
    coaching_branch = forms.ModelChoiceField(required=True, queryset=Branches.objects.all(), widget=forms.Select(attrs={'class':'my-select', 'placeholder':'Choose a branch...'}))
    cv = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={'class':'form-control'}))

    class Meta:
        model = Coach
        fields = ['full_name', 'phone_number', 'coach_image', 'coaching_category', 'coaching_branch', 'cv']


class PlayerForm(forms.ModelForm):
    full_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder':'Full Name', 'class':'form-control'}))
    date_of_birth = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder':'Date of Birth', 'class':'form-control'}))
    home_address = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder':'Home Address', 'class':'form-control'}))
    school_attended = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder':'School Attended', 'class':'form-control'}))
    player_position = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder':'Player Position', 'class':'form-control'}))
    player_image = forms.ImageField(required=True, widget=forms.ClearableFileInput(attrs={'class':'custom-image-field'}))
    birth_certificate = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={'class':'form-control'}))
    player_category = forms.ModelChoiceField(required=True, queryset=Categories.objects.all(), widget=forms.Select(attrs={'class':'my-select', 'placeholder':'Choose a category...'}))
    player_branch = forms.ModelChoiceField(required=True, queryset=Branches.objects.all(), widget=forms.Select(attrs={'class':'my-select', 'placeholder':'Choose a branch...'}))
    medical_condition = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'medical-condition-checkbox'}))
    medical_condition_details = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'medical-condition-details'}))
    parent_full_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder':'Parent Full Name', 'class':'form-control'}))
    parent_phone_number = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder':'Parent Phone Number', 'class':'form-control'}))
    emergency_contact = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder':'Emergency Contact', 'class':'form-control'}))
    email_address = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder':'Email Address', 'class':'custom-email-input form-control'}))

    class Meta:
        model = Player
        fields = ['full_name', 'date_of_birth', 'home_address', 'school_attended', 'player_position', 'player_image', 'birth_certificate', 'player_category', 'player_branch', 'medical_condition', 'medical_condition_details' ,'parent_full_name', 'parent_phone_number', 'emergency_contact', 'email_address']

    def clean(self):
        cleaned_data = super().clean()
        medical_condition = cleaned_data.get('medical_condition')
        if medical_condition:
            medical_condition_details = cleaned_data.get('medical_condition_details')
            if medical_condition_details == '':
                self.add_error('medical_condition_details', 'Please provide details for the medical condition.')
        else:
            pass
        return cleaned_data
    

class AttendanceForm(forms.Form):
    def __init__(self, *args, **kwargs):
        players = kwargs.pop('players')
        super().__init__(*args, **kwargs)
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