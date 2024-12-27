from django import forms
from .models import Rota, Request, StaffProfile
from django.contrib.auth.models import User

class RotaForm(forms.ModelForm):
    """
    Form for creating and updating rota entries.
    """
    class Meta:
        model = Rota
        fields = ['user', 'date', 'shift_type', 'start_time', 'end_time']  
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'end_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'shift_type': forms.Select(attrs={'class': 'form-control'}),
        }
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # Customize the user dropdown
            self.fields['user'].queryset = User.objects.all()
            self.fields['user'].label_from_instance = lambda obj: f"{obj.get_full_name()} ({obj.username})"

class RequestForm(forms.ModelForm):
    """
    Form for staff to submit a request.
    """
    class Meta:
        model = Request
        fields = ['date', 'comment']  # Fields staff can fill out
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }


class StaffCreationForm(forms.ModelForm):
    """
    Form for the admin to create staff user accounts.
    """
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    is_staff = forms.BooleanField(required=False, label="Grant Admin Access")

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'is_staff']  
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


class StaffProfileForm(forms.ModelForm):
    """
    Form for additional staff profile details.
    """
    class Meta:
        model = StaffProfile
        fields = ['full_name', 'address', 'email', 'phone_number', 'job_title'] 
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'job_title': forms.TextInput(attrs={'class': 'form-control'}),
        }