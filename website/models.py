from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager


class User(AbstractUser):
	objects = UserManager()

	phone = models.CharField(max_length=15, null=True, blank=True)
	skype = models.CharField(max_length=50, null=True, blank=True)
	# TODO: add image
