from django.shortcuts import render
from .models import Project
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required
def projects(request):
    projects = Project.objects.filter(publish=True)  # Query projects that are marked as published
    context = {
        'projects': projects,
    }
    return render(request, "projects.html", context)
