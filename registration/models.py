from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import timedelta
from datetime import datetime, date, time, timedelta
from django.apps import apps
from reservation.models import Reservation


class UsuarioProfile(AbstractUser):
    name = models.CharField(max_length=200, default='',) 
    last_name = models.CharField(max_length=200, default='')
    email = models.EmailField(max_length=254, unique=True, default='')
    bornDate = models.DateField('Fecha de nacimiento', null=True, blank=True,)
    phoneNumber = models.CharField(max_length=20, blank=True)
    role = models.CharField(max_length=100, default='tenant')
    state = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'{self.name} {self.last_name}'
    
class Tenant(UsuarioProfile):
    fieldsNetWorth = models.FloatField(default=0.0)
    clubName = models.CharField(max_length=200, default='')
    clubDescription = models.CharField(max_length=200, default='')
    clubPhoto = models.ImageField(upload_to='club_photos', null=True, blank=True) 
    clubAddress = models.CharField(max_length=200, default='')
    clubApertureTime = models.TimeField('Hora de apertura', null=True, blank=True,)
    clubClosureTime = models.TimeField('Hora de cierre', null=True, blank=True,)

    class Meta:
        verbose_name = 'Tenant'
        verbose_name_plural = 'Tenants'

    def get_available_times(self):
        print(f"Aperture time: {self.clubApertureTime}")
        print(f"Closure time: {self.clubClosureTime}")

        times = []
        current_time = self.clubApertureTime
        while current_time != self.clubClosureTime:
            times.append(current_time)
            current_time = (datetime.combine(date.today(), current_time) + timedelta(hours=1)).time()
            if current_time > time(23, 59):  # Si la hora actual supera la medianoche, resetéala a 00:00:00
                current_time = time()
        #
        return times
    
    def get_available_times_for_date(self, selected_date):
        if isinstance(selected_date, str):
            selected_date = datetime.strptime(selected_date, "%Y-%m-%d").date()

        available_times = []

        Reservation = apps.get_model('reservation', 'Reservation')
        reservations = Reservation.objects.filter(dateAtReservation=selected_date)

        reserved_times = [reservation.time for reservation in reservations]

        all_times = self.get_available_times()

        available_times = [datetime.time(t.hour, t.minute) for t in available_times]

        return available_times

class Client(UsuarioProfile):
    fieldsRented = models.ManyToManyField('FieldRentHistory', related_name='clients')

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'

class FieldRentHistory(models.Model):
    takenBy = models.ForeignKey(Client, on_delete=models.CASCADE)
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
