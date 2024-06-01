from django import forms

from altar.models.branch import Branches
from altar.models.category import Categories
from altar.models.players import Player

# Create here
class PlayerForm(forms.ModelForm):
    full_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder':'Full Name', 'class':'form-control'}))
    date_of_birth = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder':'Date of Birth', 'class':'form-control'}), label='Date of Birth',)
    home_address = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder':'Home Address', 'class':'form-control'}))
    school_attended = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder':'School Attended', 'class':'form-control'}))
    player_position = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder':'Player Position', 'class':'form-control'}))
    player_image = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'class':'custom-image-field'}))
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