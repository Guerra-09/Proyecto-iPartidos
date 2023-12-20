from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.views import LoginView
from django.views.generic.detail import DetailView
from django.contrib.auth import get_user_model
from django.contrib import messages
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
from .models import Reservation
from canchas.models import Field
from django.db import transaction
from datetime import datetime
from reservation.utils import get_all_possible_times_for_a_day
from django.utils import timezone
from django.http import HttpResponse



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


# User Recovery password view
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

                message = f'Hola, esta es tu nueva clave provisioria: {new_password} \nAsegurate de cambiarla desde Editar perfil.' 
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


# User History View
def user_reserves(request, pk):
    user = request.user 
    field_rent_history = FieldRentHistory.objects.filter(takenBy=user.id).order_by('-created_at')
    reservation_history = ReservationHistory.objects.filter(client=request.user).order_by('-created_at')
    


    reservation_ids = []
    context = []
    
    for field_rent in field_rent_history:
        reservation_ids.append(field_rent.reservation.id)



    reservation_ids = list(reversed(reservation_ids))

    print(reservation_ids.reverse())

    for i in range(len(field_rent_history)):
        field_rent = field_rent_history[i]
        reservation = reservation_history[i]

        context.append({
            'reservationHistory_id' : field_rent.id,
            'status':field_rent.reservation.status,
            'name': field_rent.reservation.field.name,
            'price': field_rent.reservation.price,
            'date': field_rent.reservation.dateToReservate,
            'id': reservation_ids[i],
            'reservation_history': reservation
        })


    for reservation in reservation_history:
        if reservation.dateToReservate < timezone.now() and reservation.status != 'cancelled':
            reservation.status = 'completed'
            reservation.save()

    return render(request, 'registration/user_reserves.html', {'context': context})








# Cambio de reserva se hace aqui y se valida en otro lado !!!!!!!!!!!!!!!

def change_reservation(request, reservation_id):

    reservation = get_object_or_404(ReservationHistory, id=reservation_id)
    field = reservation.field
    tenant = field.tenant
    today = timezone.now().date()
    selected_date = today
    available_times = []

    if request.method == 'POST':

        if 'date' in request.POST:
            selected_date_str = request.POST.get('date')
            selected_date = timezone.make_aware(datetime.strptime(selected_date_str, "%Y-%m-%d"))
            request.session['field_id'] = field.id
            request.session['date'] = selected_date_str

        if 'time' in request.POST:
            field_id = request.POST.get('field_id')
            time = request.POST.get('time')
            date_str = request.POST.get('date')
            date = timezone.make_aware(datetime.strptime(date_str, "%Y-%m-%d"))
            return redirect('confirm_reservation', reservation_id=reservation_id)
        
        
        # return render(request, 'registration/change_reservation.html', {
        #     'reservation': reservation,
        #     'field': field,
        #     'tenant': tenant,
        #     'selected_date': selected_date,
        #     'available_times': available_times,
        # })
        



    reservations = FieldRentHistory.objects.filter(
        reservation__field=field, 
        reservation__dateToReservate__date=selected_date, 
        reservation__status__in=['pending'] 
    )

    reserved_times = reservations.values_list('reservation__dateToReservate__time', flat=True)
    reserved_times = [t.strftime('%H:%M') for t in reserved_times]
    all_times = get_all_possible_times_for_a_day(tenant)
    available_times = [t for t in all_times if t not in reserved_times]

    return render(request, 'registration/reservation_update.html', {'field': field, 'available_times': available_times, 'selected_date': selected_date,  'reservation_id' : reservation_id})



def confirm_reservation(request, reservation_id):

    reservation_history = get_object_or_404(ReservationHistory, id=reservation_id)
    reservation = get_object_or_404(Reservation, id=reservation_id)
    
    
    date_str = request.POST.get('date')
    if date_str:
        date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
    else:
        HttpResponse('puxa')

    new_date_str = request.GET.get('date')
    new_time_str = request.GET.get('time')
    new_date = datetime.strptime(new_date_str, "%Y-%m-%d").date()
    new_time = datetime.strptime(new_time_str, "%H:%M").time()
    date_to_reservate = timezone.make_aware(datetime.combine(new_date, new_time))

    print(reservation.id)
    print(reservation_history.id)
    print(reservation_id)
    print(reservation.dateToReservate)
    print(date_to_reservate)

    new_reservation = Reservation(
            field=reservation.field,
            dateAtReservation=timezone.now(),
            dateToReservate=date_to_reservate,
            price=reservation.price,
            status='pending'
        )

    new_reservation_history = ReservationHistory(
        client=reservation_history.client,
        field=reservation_history.field,
        dateAtReservation=timezone.now(),
        dateToReservate=date_to_reservate,
        price=reservation_history.price,
        status='pending'
    )

    if request.method == 'POST':

        reservation_history.status = 'cancelled'
        reservation.status = 'cancelled'
        reservation_history.save()
        reservation.save()

    

        new_reservation.save()
        new_reservation_history.save()

        new_field_rent_history = FieldRentHistory(
            takenBy=reservation_history.client,
            reservation=new_reservation,
        )

        new_field_rent_history.save()


        return redirect('user_reserves', pk=reservation_history.client.id)
        
    return render(request, 'registration/reservation_update_confirmation.html', {'reservation_id': reservation_id, 'previous_reserve' : reservation , 'new_reserve' : new_reservation})




@login_required
def cancel_reservation(request, reservation_id):

    reservation_history = get_object_or_404(ReservationHistory, id=reservation_id)
    reservation = get_object_or_404(Reservation, id=reservation_id)

    if request.method == 'POST':
        reservation_history.status = 'cancelled'
        reservation_history.save()

        reservation.status = 'cancelled'
        reservation.save()

        print(f'After cancellation: {reservation_history.status}')
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


