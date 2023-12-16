from django.db import models
from registration.models import UsuarioProfile


class Field(models.Model):

    GROUND_CHOICES = (
        ('Pasto sintético', 'Pasto sintético'),
        ('Pasto real', 'Pasto real'),
        ('Cemento', 'Cemento'),
        ('Arcilla', 'Arcilla')
    )
    
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, default='', null=True, blank=True)
    description = models.CharField(default='not defined', choices=GROUND_CHOICES, max_length=100, null=True, blank=True)
    groundType = models.CharField(max_length=100, default='', null=False, blank=True)
    fieldPhoto = models.ImageField(upload_to='field_photos', null=True, blank=True) 
    price = models.IntegerField()
    isActive = models.BooleanField(default=True)
    playersPerSide = models.IntegerField(default=0)  # Provide a default value
    tenant = models.ForeignKey('registration.Tenant', on_delete=models.CASCADE, related_name='tenant_fields', null=True)
    

    def __str__(self):
        
        if self.isActive == True:
            return f'{self.tenant.clubName} - {self.name} - Activa'
        else:
            return f'{self.tenant.clubName} - {self.name} - Inactiva'


