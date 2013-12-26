from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import UserManager

class User(AbstractBaseUser):
	objects = UserManager()
	
	email = models.EmailField(max_length=254, unique=True)
	phone = models.CharField(max_length=15, null=True, blank=True)
	# TODO: add image
	 
	USERNAME_FIELD = 'email'
