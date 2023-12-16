from django.shortcuts import render
from canchas.models import Field
from .models import Reservation
from registration.models import ReservationHistory 
from registration.models import Client
from django.utils import timezone
from django.shortcuts import render, redirect
from registration.models import FieldRentHistory
from django.http import HttpResponseRedirect
from datetime import datetime, date, time


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



    reservations = ReservationHistory.objects.filter(field=field, dateToReservate__date=selected_date, status='pending').exclude(status='cancelled')
    reserved_times = reservations.values_list('dateToReservate__time', flat=True)
    reserved_times = [t.strftime("%H:%M") for t in reserved_times]

    available_times = tenant.get_available_times_for_date(selected_date)


    available_times = [t.strftime('%H:%M') for t in available_times]
    available_times = [t for t in available_times if t not in reserved_times]

    print(f"Available times: {available_times}")
    print(f"Reserved times: {reserved_times}")


    return render(request, 'reservation/reservation_menu.html', {'field': field, 'available_times': available_times, 'selected_date': selected_date})

def payment(request):
    if request.method == 'POST' or request.session.get('field_id'):
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
                'players' : field.playersPerSide
            }

            return render(request, 'reservation/reservation_payment.html', context)
        else:
            return render(request, 'reservation/reservation_error.html', {'message': 'Date or time not provided'})

    else:
        return render(request, 'reservation/reservation_payment.html')

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

            reservations = Reservation.objects.filter(field=field, dateToReservate__date=date, status__in=['confirmed', 'completed'])

            available_times = field.tenant.get_available_times_for_date(date)
            available_times = [t for t in available_times if t not in [r.dateToReservate.time() for r in reservations]]
            
            if time not in available_times:
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

            return redirect('payment_success')

        else:
            return render(request, 'reservation/reservation_error.html', {'message': 'Date or time not provided'})

    else:
        return redirect('payment')

def payment_success(request):
    return render(request, 'reservation/reservation_payment_success.html')

