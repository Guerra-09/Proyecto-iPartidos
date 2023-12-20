from django import forms
from .models import Field

GROUND_CHOICES = (('Pasto sintético', 'Pasto sintético'), ('Pasto real', 'Pasto real'), ('Cemento', 'Cemento'), ('Arcilla', 'Arcilla'))

class FieldForm(forms.ModelForm):

    class Meta:
        model = Field
        fields = ['name', 'price', 'description', 'groundType', 'playersPerSide', 'fieldPhoto',  'isActive']
        widgets = {
            'name' : forms.TextInput(attrs={'class': 'form-control'}),
            'price' : forms.NumberInput(attrs={'class': 'form-control'}),
            'isActive' : forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'description' : forms.TextInput(attrs={'class': 'form-control'}),
            'playersPerSide' : forms.NumberInput(attrs={'class': 'form-control'}),
            'fieldPhoto' : forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'groundType': 'Tipo de suelo',
        }

    def __init__(self, *args, **kwargs):
        super(FieldForm, self).__init__(*args, **kwargs)
        self.fields['groundType'] = forms.ChoiceField(choices=GROUND_CHOICES, label="Tipo de suelo")
