from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now

class User(AbstractUser):
    pass

class Project(models.Model):
    title = models.CharField(max_length=280, default=None, null=True, blank=True)
    notifications = models.EmailField(max_length=254, default=None, null=True, blank=True, help_text='Project manager email.')

class Phase(models.Model):
    name = models.CharField(max_length=280, default=None, null=False, blank=False),
    start_date = models.DateTimeField(auto_now=False, auto_now_add=False),
    end_date = models.DateTimeField(auto_now=False, auto_now_add=False),
    completed = models.BooleanField(default=False)
