from django.db import models
from django.contrib.auth.models import AbstractUser

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

class Client(UsuarioProfile):
    fieldsRented: models.ManyToManyField('FieldRentHistory')

class FieldRentHistory(models.Model):
    takenBy = models.ForeignKey(Client, on_delete=models.CASCADE)
    reservation = models.OneToOneField('Reservation', on_delete=models.CASCADE)

class Reservation(models.Model):
    field = models.ForeignKey('canchas.Field', on_delete=models.CASCADE)
    dateAtReservation = models.DateField()
    dateToReservate = models.DateField()
    price = models.FloatField()

