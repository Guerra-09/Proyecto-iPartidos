from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.views import LoginView
from .models import UsuarioProfile
from .forms import CustomUserCreationForm

from django import forms


# Create your views here.
class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/sign_up.html'
    success_url = reverse_lazy('login')

    def get_form(self, form_class=None):
        form = super(SignUpView, self).get_form()
        form.fields['username'].widget = forms.TextInput(attrs={'class': 'form-control'})
        form.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control'})
        form.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control'})
        form.fields['email'].widget = forms.EmailInput(attrs={'class': 'form-control'})
        form.fields['name'].widget = forms.TextInput(attrs={'class': 'form-control'})
        form.fields['last_name'].widget = forms.TextInput(attrs={'class': 'form-control'})
        return form
    
# class ProfileUpdate(UpdateView):
#     form_class = UsuarioForm
#     success_url = reverse_lazy('profile')
#     template_name = 'registration/profile.html'

#     def get_object(self):
#         profile, created = UsuarioProfile.objects.get_or_create(user = self.request.user)
#         return profile
    

    
class CustomLoginView(LoginView):
    template_name = 'registration/login.html'  # Asegúrate de tener la plantilla adecuada aquí

    def get_success_url(self):
        return reverse_lazy('home') 