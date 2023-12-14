from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.views import LoginView
from django.views.generic.detail import DetailView
from django.contrib.auth import get_user_model
from .models import Tenant, Client
from .forms import CustomUserCreationForm, CustomAuthenticationForm, CustomUserChangeForm
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.contrib.auth import authenticate 

# User Register View
class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/sign_up.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        if email is None:
            form.add_error('email', 'Email must be set.')
            return self.form_invalid(form)
    
        if get_user_model().objects.filter(username=email).exists():
            form.add_error('username', 'A user with that email already exists.')
            return self.form_invalid(form)

        print("Tenant created with success")

        return super().form_valid(form)
        
        
# User Profile View    
class ProfileUpdateView(UpdateView):
    model = get_user_model()
    template_name = 'registration/profile.html'
    form_class = CustomUserChangeForm
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user
    


class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'registration/login.html'

    def get_success_url(self):
        return reverse_lazy('home')
    