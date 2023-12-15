from django.db import models

# Create your models here.
class Reservation(models.Model):
    field = models.ForeignKey('canchas.Field', on_delete=models.CASCADE)
    dateAtReservation = models.DateTimeField()
    dateToReservate = models.DateTimeField()
    price = models.FloatField()
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('completed', 'Completed')], default='confirmed')  

    def __str__(self) -> str:
        return f'{self.field} {self.status}'