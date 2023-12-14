from django.shortcuts import render
from canchas.models import Field


# Create your views here.
def index(request, field_id):
    field = Field.objects.get(id=field_id)  # Obtén el campo seleccionado
    tenant = field.tenant  # Obtén el tenant correspondiente
    available_times = tenant.get_available_times()
    return render(request, 'reservation/reservation_menu.html', {'available_times': available_times})

def payment(request):
    return render(request, 'reservation/reservation_payment.html')


def payment_success(request):
    return render(request, 'reservation/reservation_payment_success.html')