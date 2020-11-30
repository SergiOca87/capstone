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

    if request.method == "POST":
        # If it has name, then it's a postmfrom the Phases form
        if 'name' in request.POST:
            name  = request.POST["name"]
            start_date = request.POST.get("start")
            end_date = request.POST.get("end")
            completed = request.POST.get("completed")
            completed = True if completed == 'on' else False
            project = Project.objects.get(pk=project_id)

            f = Phase( name = name, start_date = start_date, end_date = end_date, completed = completed, project = project)
            f.save()

            return render(request, "project.html", {
                "project": project,
                "phases": phases,
                "project_users": project_users
                # "project_users_list": project_users_list
            })
  
    # elif request.method == "PUT":
    #     print('put')
    #     data = json.loads(request.body)
    #     return HttpResponse(status=204)

        # Else, the post is from the complete or not complete toggle button
        # THis works, but reloads the page!
        # else:
        #     if( 'completed' in request.POST ):
        #         phase_id = request.POST.get("phase_id")
        #         phase = Phase.objects.get(pk=phase_id)
        #         phase.completed = False
        #         phase.save()

        #         return render(request, "project.html", {
        #             "project": project,
        #             "phases": phases,
        #             "project_users": project_users
        #             # "project_users_list": project_users_list
        #         })
        #         # "project_users_lipkst": project_users_list
        
        #     else:
        #         phase_id = request.POST.get("phase_id")
        #         phase = Phase.objects.get(pk=phase_id)
        #         phase.completed = True

        #         phase.save()
            
        #         return render(request, "project.html", {
        #             "project": project,
        #             "phases": phases,
        #             "project_users": project_users
        #             # "project_users_list": project_users_list
        #         })
    else:
        try:
            project = Project.objects.get(pk=project_id)
        except Project.DoesNotExist:
            return JsonResponse({"error": "Project not found."}, status=404)

        return render(request, "project.html", {
            "project": project,
            "phases": phases,
            "project_users": project_users
        })


def phase(request, phase_id):
    if request.method == "PUT":
        data = json.loads(request.body)
        phase = Phase.objects.get(pk=phase_id)
        print(data)
        if data.get('completed') == 'True':
            phase.completed = True
            phase.save()
        elif data.get('completed') == 'False':
            phase.completed = False
            phase.save()
        return HttpResponse(status=204)

    
# Before editing the project, logo and users must work well
def edit_project(request, project_id):
    if request.method == "POST":
        # project = Project.objects.get(pk=project_id)

        # title = request.POST["title"]
        # current_user = request.user
        # project_users_id = request.POST.getlist('users')
        # project_users_list = []
        # project_logo = request.POST["project_logo"]
        # # Change logo when it works as well

        # project.title = title

        # ?
        # # project.project_users 

        # title = request.POST["title"]
       

        # project.title = request.POST["title"]
        # project.notifications = request.POST["notifications"]

        # project.save();
   
        return HttpResponseRedirect(reverse('project_list'))
    else:

        # Need to create an edit template and pre-populate fields
        project = Project.objects.get(pk=project_id)
        return render(request, "dashboard.html", {
            "project": project
        })

# Projects really need a list of users assigned to that project to work well
# Make restrictions (edit button, show all projects...Maybe a user level)
# Able to mark a phase as completed
# Email notifications? That would be an extra
# project.html needs a list of users with access to that project, so let's use "project_users"
