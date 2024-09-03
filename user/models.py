from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

# Create your models here.


phone_validator = RegexValidator(regex=r'^\d{1,14}$', message="El número de teléfono solo puede contener hasta 14 dígitos.")

class User(AbstractUser):
    picture = models.ImageField(default='profile_default.png', upload_to='users/')
    location = models.CharField(max_length=60, null= True, blank=True)
    number_phone = models.CharField(max_length=14, 
        validators=[phone_validator], 
        null=True, 
        blank=True)