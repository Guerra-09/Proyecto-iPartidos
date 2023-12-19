from django.db import models
from registration.models import UsuarioProfile, Tenant
from datetime import datetime
from django.apps import apps
from datetime import time


class Field(models.Model):

    GROUND_CHOICES = (
        ('Pasto sintético', 'Pasto sintético'),
        ('Pasto real', 'Pasto real'),
        ('Cemento', 'Cemento'),
        ('Arcilla', 'Arcilla')
    )
    
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name='Nombre de cancha', max_length=100, default='', null=True, blank=True)
    description = models.CharField(verbose_name='Descripcion' ,default='', max_length=100, null=True, blank=True)
    groundType = models.CharField(verbose_name='Tipo de suelo' ,max_length=100, default='Pasto sintético', choices=GROUND_CHOICES, null=False, blank=True)
    fieldPhoto = models.ImageField(verbose_name='Foto de cancha (opcional)' ,upload_to='field_photos', null=True, blank=True) 
    price = models.IntegerField(verbose_name='Precio')
    isActive = models.BooleanField(verbose_name='Cancha activa' ,default=True)
    playersPerSide = models.IntegerField(verbose_name='Jugadores por lado' ,default=0)
    opening_time = models.TimeField(default=time(14, 0))
    closing_time = models.TimeField(default=time(23, 0))
    tenant = models.ForeignKey('registration.Tenant', on_delete=models.CASCADE, related_name='tenant_fields', null=True)
    
    
    def get_available_times_for_date(self, selected_date, field):
        tenant = self.tenant
        if isinstance(selected_date, str):
            selected_date = datetime.strptime(selected_date, "%Y-%m-%d").date()

        ReservationHistory = apps.get_model('registration', 'ReservationHistory')
        reservations = ReservationHistory.objects.filter(dateToReservate__date=selected_date, field=field).exclude(status='cancelled')

        reserved_times = [reservation.dateToReservate.time() for reservation in reservations]

        all_times = tenant.get_available_times()

        available_times = [t for t in all_times if t not in reserved_times]

        return available_times


    def __str__(self):
        
        if self.isActive == True:
            return f'{self.tenant.clubName} - {self.name} - Activa'
        else:
            return f'{self.tenant.clubName} - {self.name} - Inactiva'


