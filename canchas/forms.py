from django import forms
from .models import Field

class FieldForm(forms.ModelForm):
    class Meta:
        model = Field
        fields = ['name', 'price', 'isActive']

        widgets = {
            'name' : forms.TextInput(attrs={'class': 'form-control'}),
            'price' : forms.NumberInput(attrs={'class': 'form-control'}),
        }

    # def __init__(self, *args, **kwargs):
    #     self.request = kwargs.pop('request', None)
    #     super(FieldForm, self).__init__(*args, **kwargs)
            
    # def save(self, commit=True):
    #     instance = super(FieldForm, self).save(commit=False)
    #     instance.tenant = self.request.user.tenant
    #     if commit:
    #         instance.save()
    #     return instance
            

