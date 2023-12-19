from django.db import models


class Reservation(models.Model):
    field = models.ForeignKey('canchas.Field', on_delete=models.CASCADE)
    dateAtReservation = models.DateTimeField()
    dateToReservate = models.DateTimeField()
    price = models.FloatField()
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='pending')
    def __str__(self) -> str:
        return f'#{self.id} {self.field} - {self.status} '