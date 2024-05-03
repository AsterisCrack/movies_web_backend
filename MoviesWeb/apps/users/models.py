from django.db import models
from django.contrib.auth.models import AbstractUser # Usar el modelo AbstractUser de Django (viene en la práctica)

# Create your models here.

class Usuario(AbstractUser):
    nombre = models.CharField(max_length=256)
    username = models.CharField(max_length=32, unique=True)
    tel = models.CharField(max_length=32)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
