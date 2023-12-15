from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.views import LoginView
from django.views.generic.detail import DetailView
from django.contrib.auth import get_user_model
from .models import Tenant, Client
from .forms import CustomUserCreationForm, CustomAuthenticationForm, CustomUserChangeForm, PasswordRecoveryForm
from django.contrib.auth.forms import AuthenticationForm
from django import forms 
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import PasswordResetForm
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from django.core.mail import BadHeaderError



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
    

# User Profile Login view
class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'registration/login.html'

    def get_success_url(self):
        return reverse_lazy('home')
    

def password_recovery(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            User = get_user_model()
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                user = None

            if user is not None:
                # Generar una nueva contraseña para el usuario
                new_password = User.objects.make_random_password()
                user.set_password(new_password)
                user.save()

                print("usuario con nueva contrasena")

                message = 'Tu nueva contraseña es: ' + new_password
                email = 'djangoa353@gmail.com'
                name = 'pepe'

                send_mail(
                    'Contact form', #title
                    message,
                    'settings.EMAIL_HOST_USER',
                    [email],
                    fail_silently=False,
                )

                return render(request, 'registration/password_sent.html')



    else:
        form = PasswordResetForm()
    
    return render(request, 'registration/password_recovery.html', {'form': form})

