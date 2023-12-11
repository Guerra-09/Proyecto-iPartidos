# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Tenant, Client
from django.forms import CheckboxInput

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, initial=' @gmail.com')
    name = forms.CharField(max_length=200, initial='prueba')
    last_name = forms.CharField(max_length=200, initial='prueba')
    bornDate = forms.DateField(initial='2000-01-01')
    phoneNumber = forms.CharField(max_length=20, initial='1234567890')
    role = forms.BooleanField(required=False)
    
    class Meta:
        model = Tenant
        fields = ['name', 'last_name', 'email', 'password1', 'password2', 'bornDate', 'phoneNumber', 'role']

        widgets = {
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'bornDate': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'phoneNumber': forms.TextInput(attrs={'class': 'form-control'}),
            'role': CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'role': 'Registrar un club',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['role'].required = False

    def clean_email(self):
        email = self.cleaned_data['email']
        if Tenant.objects.filter(email=email).exists():
            raise forms.ValidationError('Este correo electrónico ya está en uso.')
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        if self.cleaned_data.get('role') == True:
            user.role = 'tenant'
        else:
            user.role = 'client'
        if commit:
            user.save()
        return user
        
        if commit:
            user.save()
            if user.role == 'tenant':
                print("ES UN TENANT")
                
        return user
