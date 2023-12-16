from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.views import LoginView
from django.views.generic.detail import DetailView
from django.contrib.auth import get_user_model
from .models import Tenant, Client, FieldRentHistory, ReservationHistory
from .forms import CustomUserCreationForm, CustomAuthenticationForm, CustomUserChangeForm, PasswordRecoveryForm
from django.contrib.auth.forms import AuthenticationForm
from django import forms 
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from decimal import Decimal, ROUND_DOWN
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages



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

                message = f'Hola, esta es tu nueva clave provisioria: {new_password} \nAsegurate de cambiarla desde Mi perfil.' 
                email = request.POST.get('email')

                send_mail(
                    'Contact form', #title
                    message,
                    'settings.EMAIL_HOST_USER',
                    [email],
                    fail_silently=False,
                )

                return render(request, 'registration/password_sent.html')
            else:

                messages.error(request, 'El correo electrónico no existe en nuestra base de datos.')
                return render(request, 'registration/password_recovery.html', {'form': form})

        

    else:
        form = PasswordResetForm()
    
    return render(request, 'registration/password_recovery.html', {'form': form})

def user_reserves(request, pk):
    user = request.user
    reservation_history = ReservationHistory.objects.filter(client=user.client).order_by('-dateToReservate')
    return render(request, 'registration/user_reserves.html', {'reservation_history': reservation_history})

    # User = get_user_model()
    # user = User.objects.get(pk=pk)
    # reservations = FieldRentHistory.objects.filter(takenBy=user)

    # if request.method == 'POST':
    #     reservation_to_delete = get_object_or_404(FieldRentHistory, pk=request.POST.get('reservation_id'))
    #     print(f"Reservation to delete: {reservation_to_delete}")
    #     print(f"User: {user}")
    #     if reservation_to_delete.takenBy.id == user.id:
    #         print("Deleting reservation")
    #         reservation = reservation_to_delete.reservation
    #         reservation.status = 'cancelled'
    #         reservation.save()

    #         # Update the reservation history
    #         reservation_history = ReservationHistory.objects.get(
    #             field=reservation.field,
    #             dateAtReservation=reservation.dateAtReservation,
    #             dateToReservate=reservation.dateToReservate,
    #             client=user.client
    #         )
    #         reservation_history.status = 'cancelled'
    #         reservation_history.save()

    #         reservation_to_delete.delete()
    #     else:
    #         print("User did not create this reservation")
    #     return HttpResponseRedirect(reverse('user_reserves', args=[str(user.pk)]))

    # return render(request, 'registration/user_reserves.html', {'reservations': reservations})

@login_required
def edit_reservation(request, reservation_id):
    reservation = get_object_or_404(ReservationHistory, id=reservation_id)
    if request.method == 'POST':
        # Aquí puedes agregar el código para editar la reserva
        # ...
        return redirect('user_reserves', pk=request.user.pk)
    

@login_required
def cancel_reservation(request, reservation_id):
    reservation = get_object_or_404(ReservationHistory, id=reservation_id)
    if request.method == 'POST':
        reservation.status = 'cancelled'
        reservation.save()
        return redirect('user_reserves', pk=request.user.pk)

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Actualiza la sesión para que no sea necesario volver a iniciar sesión
            return redirect('home')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/change_password.html', {'form': form})


