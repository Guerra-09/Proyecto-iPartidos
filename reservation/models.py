from django.db import models
from registration.models import FieldRentHistory

# Create your models here.
class Reservation(models.Model):
    field = models.ForeignKey('canchas.Field', on_delete=models.CASCADE)
    dateAtReservation = models.DateField()
    dateToReservate = models.DateField()
    price = models.FloatField()
    field_rent_history = models.OneToOneField(FieldRentHistory, on_delete=models.CASCADE, related_name='reservation')
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('completed', 'Completed')], default='pending')