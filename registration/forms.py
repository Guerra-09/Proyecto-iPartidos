# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Tenant, Client
from django.forms import CheckboxInput
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
import re
from django.core.exceptions import ValidationError


# User Register Form
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
        if Tenant.objects.filter(email=email).exists() or Client.objects.filter(email=email).exists():
            raise forms.ValidationError('Este correo electrónico ya está en uso.')
        return email
    
    def clean_phoneNumber(self):
        phoneNumber = self.cleaned_data['phoneNumber']
        if not re.match(r'^9\d{8}$', phoneNumber):
            raise ValidationError('El número debe contener 9 caracteres, incluyendo el 9 al principio.')
        
        if get_user_model().objects.filter(phoneNumber=phoneNumber).exists():
            raise ValidationError('El número ya está en uso.')

        return phoneNumber
    
    def save(self, commit=True):
        if self.cleaned_data.get('role') == True:
            user = Tenant()
            user.role = 'tenant'
        else:
            user = Client()
            user.role = 'client'
        user.username = self.cleaned_data['email']
        user.set_password(self.cleaned_data['password1'])
        user.email = self.cleaned_data['email']
        user.name = self.cleaned_data['name']
        user.last_name = self.cleaned_data['last_name']
        user.bornDate = self.cleaned_data['bornDate']
        user.phoneNumber = self.cleaned_data['phoneNumber']

        if commit:
            user.save()
        return user

# User Profile Update Form
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ['name', 'last_name', 'email', 'phoneNumber']

        widgets = { 
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phoneNumber': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(CustomUserChangeForm, self).__init__(*args, **kwargs)
        del self.fields['password']

    def clean_phoneNumber(self):
        phoneNumber = self.cleaned_data['phoneNumber']
        if not re.match(r'^9\d{8}$', phoneNumber):
            raise ValidationError('El número debe contener 9 caracteres, incluyendo el 9 al principio.')
        
        if get_user_model().objects.filter(phoneNumber=phoneNumber).exists():
            raise ValidationError('El número ya está en uso.')

        return phoneNumber
    

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = user.email  # Set username to be the same as email
        if commit:
            user.save()
        return user

# Login Auhentication Form
class CustomAuthenticationForm(AuthenticationForm):

    username = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username is not None and password:
            self.user_cache = authenticate(self.request, username=username, password=password)

        if self.user_cache is None:
            raise forms.ValidationError(
                self.error_messages['invalid_login'],
                code='invalid_login',
                params={'username': self.username_field.verbose_name},
            )
        return cleaned_data