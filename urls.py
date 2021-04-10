"""projectplanner URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("project_list", views.project_list, name="project_list"),
    path("new", views.new_project, name="new_project"),
    path("project/<int:project_id>", views.project, name="project"),
    path("phase/<int:phase_id>", views.phase, name="phase"),
    path("edit_project/<int:project_id>", views.edit_project, name="edit_project"),
    path("edit_phase/<int:phase_id>/<int:project_id>", views.edit_phase, name="edit_phase"),
    path("edit_profile/<int:user_id>", views.edit_profile, name="edit_profile"),
    path("delete_phase/<int:phase_id>/<int:project_id>", views.delete_phase, name="delete_phase")
]
