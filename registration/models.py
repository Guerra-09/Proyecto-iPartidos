from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class UsuarioProfile(AbstractUser):
    name = models.CharField(max_length=200, default='')
    last_name = models.CharField(max_length=200, default='')
    email = models.EmailField(max_length=254, unique=True, default='')
    password = models.CharField(max_length=128, default='')
    username = models.CharField(max_length=150, unique=True, default='')

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        related_name='usuario_profiles',  # Cambia 'usuario_profiles' a algo significativo
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        related_name='usuario_profiles_permissions',  # Cambia 'usuario_profiles_permissions' a algo significativo
        blank=True,
        help_text='Specific permissions for this user.',
    )

    def __str__(self) -> str:
        return f'{self.name} {self.last_name}'
    
# USER = guerra
# psswd = wakfu123