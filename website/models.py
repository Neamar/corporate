from django.db import models
from django.contrib.auth.models import AbstractBaseUser

class User(AbstractBaseUser):
    email = models.EmailField(max_length=254, unique=True)
    phone = models.CharField(max_length=15, null=True, blank=True)

    USERNAME_FIELD = 'email'
