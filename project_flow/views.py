from django.http import HttpResponse
from django.utils.html import escape
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout

from django.utils.safestring import mark_safe
from django.views.decorators.http import require_GET,require_POST,require_safe,require_http_methods
from django.contrib.auth.decorators import login_required
from .models import Project,Task,Document,Comment
from .forms import ProjectForm,TaskForm,DocumentForm,CommentForm
# Create your views here.


def dashboard(request):
    projects = Project.objects.all()
    return render(request, 'project_flow/dashboard.html', {'projects': projects})


# @login_required
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    tasks = project.tasks.all()
    documents = project.documents.all()
    return render(request, 'project_flow/project_detail.html', {'project': project, 'tasks': tasks, 'documents': documents})

# @login_required
def add_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ProjectForm()
    return render(request, 'project_flow/add_project.html', {'form': form})

# @login_required
def add_task(request, project_id):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        
        if form.is_valid():
            print(form)
            form.save()
            return redirect('project_detail', pk=project_id)
    else:
        form = TaskForm(initial={'project': project_id})
    return render(request, 'project_flow/add_task.html', {'form': form})

# @login_required
def add_comment(request, task_id):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('project_detail', pk=form.cleaned_data['task'].project.id)
    else:
        form = CommentForm(initial={'task': task_id})
    return render(request, 'project_flow/add_comment.html', {'form': form})

# @login_required
def add_document(request, project_id):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('project_detail', pk=project_id)
    else:
        form = DocumentForm(initial={'project': project_id})
    return render(request, 'project_flow/add_document.html', {'form': form})


