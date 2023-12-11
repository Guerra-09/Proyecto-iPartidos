from django.db import models
from registration.models import UsuarioProfile

class FieldCategory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    maxPlayers = models.IntegerField()

class Field(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    rentedBy = models.ForeignKey(UsuarioProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='rented_fields')
    category = models.ForeignKey(FieldCategory, on_delete=models.SET_NULL, null=True, blank=True)
    price = models.IntegerField()
    isActive = models.BooleanField(default=True)
    tenant = models.ForeignKey('registration.Tenant', on_delete=models.CASCADE, related_name='tenant_fields', null=True)
    

    def __str__(self):
        return f'{self.name} {self.isActive}'

