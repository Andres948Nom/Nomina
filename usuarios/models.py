from django.contrib.auth.models import AbstractUser
from django.db import models
from empresas.models import Empresa

class CustomUser(AbstractUser):
    TIPO_USUARIO_CHOICES = [
        ('UNICA', 'Única Empresa'),
        ('MULTIPLE', 'Múltiples Empresas'),
    ]
    email = models.EmailField(unique=True)
    tipo_usuario = models.CharField(max_length=10, choices=TIPO_USUARIO_CHOICES)
    is_first_login = models.BooleanField(default=True)
    empresa_activa = models.ForeignKey('empresas.Empresa', null=True, blank=True, on_delete=models.SET_NULL, related_name='usuarios_activos')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # Para crear usuarios desde la consola
