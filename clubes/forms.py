from django import forms
from registration.models import Tenant

class ClubForm(forms.ModelForm):
    class Meta:
        model = Tenant
        fields = ['clubName', 'clubDescription', 'clubPhoto', 'clubAddress', 'clubApertureTime', 'clubClosureTime']
        widgets = {
            'clubName': forms.TextInput(attrs={'class': 'form-control'}),
            'clubDescription': forms.TextInput(attrs={'class': 'form-control'}),
            'clubPhoto': forms.FileInput(attrs={'class': 'form-control'}),
            'clubAddress': forms.TextInput(attrs={'class': 'form-control'}),
            'clubApertureTime': forms.TimeInput(attrs={'type': 'time'}),
            'clubClosureTime': forms.TimeInput(attrs={'type': 'time'}),
        }
        labels = {
            'clubName': 'Nombre del club',
            'clubDescription': 'Descripción del club',
            'clubPhoto': 'Foto del club',
            'clubAddress': 'Dirección del club',
        }