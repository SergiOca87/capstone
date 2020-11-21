from django.contrib import admin

# Register your models here.
from .models import Project
from .models import Phase

admin.site.register(Project)
admin.site.register(Phase)