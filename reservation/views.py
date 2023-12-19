from django.shortcuts import render
from canchas.models import Field
from .models import Reservation
from .forms import PaymentForm
from registration.models import ReservationHistory 
from registration.models import Client
from django.utils import timezone
from django.shortcuts import render, redirect
from registration.models import FieldRentHistory
from datetime import datetime
from .utils import get_all_possible_times_for_a_day
from django.core.mail import send_mail
from django.core.exceptions import ValidationError

# This func gets time available and returns it to the view
def index(request, field_id):
    field = Field.objects.get(id=field_id)  
    tenant = field.tenant  
    today = timezone.now().date()
    selected_date = today

    if request.method == 'POST':

        if 'date' in request.POST:
            # Cambiar la fecha
            selected_date_str = request.POST.get('date')
            selected_date = timezone.make_aware(datetime.strptime(selected_date_str, "%Y-%m-%d"))
            request.session['field_id'] = field_id
            request.session['date'] = selected_date_str

        if 'time' in request.POST:
            # Reservar un horario
            request.session['field_id'] = field_id
            request.session['date'] = selected_date.strftime("%Y-%m-%d")
            request.session['time'] = request.POST.get('time')
            return redirect('payment')


    reservations = FieldRentHistory.objects.filter(
        reservation__field=field, 
        reservation__dateToReservate__date=selected_date, 
        reservation__status__in=['pending'] 
    )

    reserved_times = reservations.values_list('reservation__dateToReservate__time', flat=True)
    reserved_times = [t.strftime('%H:%M') for t in reserved_times]

    all_times = get_all_possible_times_for_a_day(tenant)
    print(f"All times: {all_times}")

    available_times = [t for t in all_times if t not in reserved_times]

    print(f"Available times: {available_times}")


    return render(request, 'reservation/reservation_menu.html', {'field': field, 'available_times': available_times, 'selected_date': selected_date})


def payment(request):

    #form = PaymentForm(request.POST or None) 
    if request.method == 'POST' or request.session.get('field_id'):
        form = PaymentForm(request.POST)
        if form.is_valid():
            print("Form valido")
        else:
            print('esta invalido')



        field_id = request.POST.get('field_id', request.session.get('field_id'))
        date_str = request.POST.get('date', request.session.get('date'))
        time_str = request.POST.get('time', request.session.get('time'))
        field = Field.objects.get(id=field_id)

        try:
            client = Client.objects.get(usuarioprofile_ptr=request.user)
        except Client.DoesNotExist:
            return render(request, 'reservation/reservation_error.html', {'message': 'Client does not exist'})

        if date_str and time_str:  
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
            time = datetime.strptime(time_str, "%H:%M").time()

            context = {
                'field': field,
                'date': date,
                'time': time,
                'price': field.price,
                'players' : field.playersPerSide,
                'form' : form
                
            }

            return render(request, 'reservation/reservation_payment.html', context )
        else:
            return render(request, 'reservation/reservation_error.html', {'message': 'Date or time not provided'})

    else:
        form = PaymentForm()
        return render(request, 'reservation/reservation_payment.html', {'form': form})


def create_reservation(request):

    if request.method == 'POST':

        field_id = request.session.get('field_id')
        date_str = request.session.get('date')
        time_str = request.session.get('time')
        field = Field.objects.get(id=field_id)

        try:
            client = Client.objects.get(usuarioprofile_ptr=request.user)
        except Client.DoesNotExist:
            return render(request, 'reservation/reservation_error.html', {'message': 'Client does not exist'})

        if date_str and time_str:  
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
            time = datetime.strptime(time_str, "%H:%M").time()

            date_to_reservate = timezone.make_aware(datetime.combine(date, time))

            reservations = FieldRentHistory.objects.filter(
                reservation__field=field, 
                reservation__dateToReservate__date=date, 
                reservation__status='pending'
            )

            reserved_times = reservations.values_list('reservation__dateToReservate__time', flat=True)
            reserved_times = [t.strftime("%H:%M") for t in reserved_times]
            all_times = get_all_possible_times_for_a_day(field.tenant)
            #available_times = [t for t in all_times if t not in reserved_times]
            available_times = [t for t in all_times if t not in reserved_times]

            time_str = time.strftime("%H:%M")  # Convertir a string

            if time_str not in available_times:
                return render(request, 'reservation/reservation_error.html', {'message': 'Time is not available'})

            reservation = Reservation.objects.create(
                field=field, 
                dateAtReservation=timezone.now(), 
                dateToReservate=date_to_reservate,
                price=field.price,
                status='pending' 
            )

            ReservationHistory.objects.create(
            field=reservation.field,
            dateAtReservation=reservation.dateAtReservation,
            dateToReservate=reservation.dateToReservate,
            price=reservation.price,
            status=reservation.status,
            client=request.user.client  # Assuming the User model has a 'client' field
            )

            field_rent_history = FieldRentHistory.objects.create(takenBy=client, reservation=reservation)


            message = f"""
                Hola {request.user.username},

                Tu reserva ha sido creada con éxito. Aquí están los detalles de tu reserva:

                Código de reserva: {reservation.id}
                Fecha y hora de la reserva: {reservation.dateToReservate.strftime('%d-%m-%Y %H:%M')}hrs
                Nombre de la cancha: {field.name}
                Precio pagado: {reservation.price}

                Gracias por tu reserva.
            """

            send_mail(
                'Reserva creada',  # Asunto
                message,
                'djangoa353@gmail.com',  # Change to env environment variable
                [request.user.email], 
            )

            return redirect('payment_success')

        else:
            return render(request, 'reservation/reservation_error.html', {'message': 'Date or time not provided'})

    else:
        
        form = PaymentForm()
        return render(request, 'reservation/payment')


def payment_success(request):
    return render(request, 'reservation/reservation_payment_success.html')