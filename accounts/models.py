from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class CustomUser(AbstractUser):
    email = models.EmailField(null=True, blank=True)
    country = models.CharField(max_length=50, null=True)
    city = models.CharField(max_length=50, null=True)
