from django.shortcuts import render
from .models import Project

# Create your views here.
def projects(request):
    projects = Project.objects.filter(publish=True)  # Query projects that are marked as published
    context = {
        'projects': projects,
    }
    return render(request, "pages/projects.html", context)
