from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from datetime import datetime

from .models import User, Project

def index(request):
    return render(request, "index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("list"))
        else:
            return render(request, "index.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "index.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return render(request, "dashboard.html", {
            "project": project
        })
    else:
        return render(request, "register.html")

def list(request):
    projects = Project.objects.all()
    return render(request, "list.html", {
        'projects': projects
    })


# Find projects where this user is assigned...
def dashboard(request):
    current_user = request.user
    project = Project.objects.get(pk=project_id)
    

def new_project(request):
    users = User.objects.all()
    admin = request.user
    
    if request.method == "POST":
        title = request.POST["title"]
        notifications = request.POST["notifications"]
        notifications = True if notifications == 'on' else False
        admin = request.user

        f = Project(title = title, notifications = notifications, admin = admin)
        f.save()

        admin.projects.add(f)
        # return this new project page instead
        return render(request, "project.html", {
            "project": f
        })
    else:
        return render(request, "new.html", {
            "users": users,
            "admin": admin
        })

def project(request, project_id):
    # is it pk?
    try:
        project = Project.objects.get(pk=project_id)
    except Project.DoesNotExist:
        return JsonResponse({"error": "Project not found."}, status=404)

    return render(request, "project.html", {
        "project": project
    })

    
def edit_project(request, project_id):
    if request.method == "POST":
        project = Project.objects.get(pk=project_id)

        # Change logo when it works as well

        title = request.POST["title"]
        notifications = request.POST["notifications"]

        project.title = request.POST["title"]
        project.notifications = request.POST["notifications"]

        project.save();
   
        return HttpResponseRedirect(reverse('list'))
    else:

        # Need to create an edit template and pre-populate fields
        project = Project.objects.get(pk=project_id)
        return render(request, "dashboard.html", {
            "project": project
        })

# Create a project phase form to add phases to a project
