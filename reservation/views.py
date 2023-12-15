from django.shortcuts import render
from canchas.models import Field
from .models import Reservation
from registration.models import Client
from django.utils import timezone
from django.shortcuts import render, redirect
from registration.models import FieldRentHistory
from django.http import HttpResponseRedirect
from datetime import datetime, date, time
import os



def index(request, field_id):
    field = Field.objects.get(id=field_id)  
    tenant = field.tenant  
    today = timezone.now().date()
    selected_date = today

    if request.method == 'POST':
        
        selected_date_str = request.POST.get('date')
        selected_date = datetime.strptime(selected_date_str, "%Y-%m-%d").date() 
        reservations = Reservation.objects.filter(field=field, dateToReservate__date=selected_date)
        reserved_times = reservations.values_list('dateToReservate__time', flat=True)
        
        available_times = tenant.get_available_times_for_date(selected_date)
        available_times = [time(int(t.split(':')[0]), int(t.split(':')[1])) for t in available_times]
        available_times = [t for t in available_times if t not in reserved_times]

        print(f"selected_date: {selected_date}")
        print(f"reservations: {reservations}")
        print(f"reserved_times: {reserved_times}")
        print(f"available_times: {available_times}")
    else:
        available_times = tenant.get_available_times()

    return render(request, 'reservation/reservation_menu.html', {'field': field, 'available_times': available_times, 'selected_date': selected_date})

def payment(request):
    if request.method == 'POST':
        field_id = request.POST.get('field_id')
        date_str = request.POST.get('date')
        time_str = request.POST.get('time')
        field = Field.objects.get(id=field_id)

        try:
            client = Client.objects.get(usuarioprofile_ptr=request.user)
        except Client.DoesNotExist:
            return render(request, 'reservation/reservation_error.html', {'message': 'Client does not exist'})

        if date_str and time_str:  
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
            time = datetime.strptime(time_str, "%H:%M").time()


            date_to_reservate = datetime.combine(date, time)

            reservations = Reservation.objects.filter(field=field, dateToReservate__date=date)

            available_times = field.tenant.get_available_times_for_date(date)
            print("Available times after get_available_times_for_date:", available_times)

            available_times = [time(int(t.split(':')[0]), int(t.split(':')[1])) for t in available_times]
            print("Available times after conversion to datetime.time objects:", available_times)

            available_times = [t for t in available_times if t not in [r.dateToReservate.time() for r in reservations]]
            print("Available times after removing reserved times:", available_times)


            available_times = field.tenant.get_available_times_for_date(date)
            available_times = [time(int(t.split(':')[0]), int(t.split(':')[1])) for t in available_times]
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

            field_rent_history = FieldRentHistory.objects.create(takenBy=client, reservation=reservation)

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

def payment_success(request):
    return render(request, 'reservation/reservation_payment_success.html')


