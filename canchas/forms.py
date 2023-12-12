from django import forms
from .models import Field

class FieldForm(forms.ModelForm):
    class Meta:
        model = Field
        fields = ['name', 'price', 'isActive']

        widgets = {
            'name' : forms.TextInput(attrs={'class': 'form-control'}),
            'price' : forms.NumberInput(attrs={'class': 'form-control'}),
            'isActive' : forms.CheckboxInput(attrs={'class': 'form-control'}),      
        }
            
        

