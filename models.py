from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime
from django.utils.timezone import now

class User(AbstractUser):
    projects = models.ManyToManyField('Project', blank=True, related_name="projects")
    avatar = models.ImageField(default=None, null=True, blank=True)

class Project(models.Model):
    title = models.CharField(max_length=280, default=None, null=True, blank=True)
    # notifications = models.BooleanField(default=None, null=True, blank=True, help_text='If enabled, users related to this project will get e-mail notifications.')
    # users = models.ManyToManyField(User, blank=True, related_name="users")
    project_logo = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=100, default=None, null=True, blank=True)
    admin = models.ForeignKey(User, related_name="admin", default=None, null=True, blank=True, on_delete=models.CASCADE)
    project_users = models.ManyToManyField(User, blank=True, related_name="project_users")

class Phase(models.Model):
    name = models.CharField(max_length=280, default=None, null=True, blank=True)
    start_date = models.DateField(auto_now=False, auto_now_add=False)
    end_date = models.DateField(auto_now=False, auto_now_add=False)
    completed = models.BooleanField(default=None, null=True, blank=True)
    project = models.ForeignKey(Project, related_name="project", default=None, null=True, blank=True, on_delete=models.CASCADE)
