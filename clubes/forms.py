from django import forms
from registration.models import Tenant
import datetime

HOUR_CHOICES = [(datetime.time(i).strftime('%H:%M'), '{:02d}:00'.format(i)) for i in range(24)]


class ClubForm(forms.ModelForm):

    clubApertureTime = forms.ChoiceField(choices=HOUR_CHOICES, label='Hora de apertura del club')
    clubClosureTime = forms.ChoiceField(choices=HOUR_CHOICES, label='Hora de cierre del club')
    


    class Meta:
        model = Tenant
        fields = ['clubName', 'clubDescription', 'clubPhoto', 'clubAddress', 'clubApertureTime', 'clubClosureTime']
        widgets = {
            'clubName': forms.TextInput(attrs={'class': 'form-control'}),
            'clubDescription': forms.TextInput(attrs={'class': 'form-control'}),
            'clubPhoto': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'clubAddress': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'clubName': 'Nombre del club',
            'clubDescription': 'Descripción del club',
            'clubPhoto': 'Foto del club',
            'clubAddress': 'Dirección del club',
        }