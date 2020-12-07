import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt

from .models import User, Project, Phase

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
            return HttpResponseRedirect(reverse("index"))
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
        user_color = request.POST["user_color"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, user_color, password)
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

def edit_profile(request, user_id):
    user = request.user
    if request.method == "POST":
        user.username = request.POST["username"]
        user.user_color = request.POST["user_color"]

        print(user.user_color)
    
        # Attempt to change user fields
        try:
            user.save()
        except IntegrityError:
            return render(request, "edit_profile.html", {
                "message": "Username already taken."
            })
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    else:
        return render(request, "edit_profile.html", {
            "user": user
        })


def project_list(request):
    user = request.user
    user_projects = user.projects.all()
    return render(request, "project_list.html", {
        'user_projects': user_projects,
        'user': user
    })


# Find projects where this user is assigned...
# Add an avatar, edit name maybee?
# Able to edit your account I guess
def dashboard(request, project_id):
    current_user = request.user
    project = Project.objects.get(pk=project_id)
    

def new_project(request):
    users = User.objects.all()
    current_user = request.user
    
    if request.method == "POST":
        title = request.POST["title"]
        project_users_id = request.POST.getlist('users')
        project_logo = request.POST["project_logo"]

        f = Project(title = title, admin = current_user, project_logo = project_logo)
        f.save()

        # Add this project, to the current user list of projects
        current_user.projects.add(f)
        
        for user_id in project_users_id:
            # Add the project to the selected users projects list
            user = User.objects.get(pk=user_id)
            user.projects.add(f)

            # Add the user to the project list of users
            f.project_users.add(user)

        # Get a QuerySet of the project users
        project_users = f.project_users.all()
        # print(project_users_list)

        # return this new project page instead
        return render(request, "project.html", {
            "project": f,
            "project_users": project_users
        })
    else:
        return render(request, "new.html", {
            "users": users,
            "current_user": current_user
        })

# @csrf_exempt
def project(request, project_id):
    project = Project.objects.get(pk=project_id)
    phases = Phase.objects.filter(project=project)
    project_users = project.project_users.all()
    all_phases = Phase.objects.all()
    latest_phase_id = Phase.objects.last().id + 1

    if request.method == "POST":
        # If it has name, then it's a postmfrom the Phases form
        # Make it a POST via fetch
        data = json.loads(request.body)
        name = data.get("name")
        start_date = data.get("start")
        end_date = data.get("end")
        # completed = data.get("completed")
        # completed = True if completed == 'true' else False
        project = Project.objects.get(pk=project_id)

        f = Phase( name = name, start_date = start_date, end_date = end_date, completed = False, project = project, id=latest_phase_id)
        f.save()

        # Now retrieve the id of this newly created Phase, needed to create the template literal
        return HttpResponse(status=204)


    else:
        try:
            project = Project.objects.get(pk=project_id)
        except Project.DoesNotExist:
            return JsonResponse({"error": "Project not found."}, status=404)

        return render(request, "project.html", {
            "project": project,
            "phases": phases,
            "latest_phase_id": latest_phase_id,
            "project_users": project_users
        })


def edit_project(request, project_id):
    project = Project.objects.get(pk=project_id)
    users = User.objects.all()
    if request.method == "POST":
        title = request.POST["title"]
        project.project_logo = request.POST["project_logo"]

        project.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return render(request, "edit_project.html", {
            "project": project,
            "users": users
        })


def phase(request, phase_id):
    if request.method == "PUT":
        data = json.loads(request.body)
        phase = Phase.objects.get(pk=phase_id)
        if data.get('completed') == 'True':
            phase.completed = True
            phase.save()
        elif data.get('completed') == 'False':
            phase.completed = False
            phase.save()
        return HttpResponse(status=204)

    else:
        phase = Phase.objects.get(pk=phase_id)
        name = phase.name
        start_date = phase.start_date
        end_date = phase.end_date
        completed = phase.completed
        return JsonResponse(
            {
                'id': phase_id,
                'name': name,
                'start_date': start_date,
                'end_date': end_date,
                'completed': completed
            }
        )

def edit_phase(request, phase_id):
    phase = Phase.objects.get(pk=phase_id)

    if request.method == "POST":
        phase_name = request.post['name']
        start_date = request.post['start_date']
        end_date = request.post['end_date']

        phase.save()
        # Returns to the previous page
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return render(request, "edit_phase.html", {
            "phase": phase
        })


def delete_phase(request, phase_id):
    phase = Phase.objects.get(pk=phase_id)
    # project = Project.objects.filter(project=phase.id)

    # Need to polish this redirect, how do I go back to the project?

    phase.delete()
    # Returns to the previous page
    return render(request, "index.html")


# Need to polish this redirect, how do I go back to the project after delete
