from django.http import HttpResponse
from django.utils.html import escape
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.http import Http404
from django.utils.safestring import mark_safe
from django.views.decorators.http import require_GET,require_POST,require_safe,require_http_methods
from django.contrib.auth.decorators import login_required
from .models import Project,Task,Document,Comment
from .forms import ProjectForm,TaskForm,DocumentForm,CommentForm
from users.models import User
# Create your views here.


def project_list(request):
    projects = Project.objects.all()
    return render(request, 'project_flow/project_list.html', {'projects': projects})

@login_required
def project_detail(request,pk):
    project=get_object_or_404(Project,pk=pk)
    member_usernames=project.members.values_list('username',flat=True)
    tasks_with_assignee=[]
    for task in project.tasks.all():
        assignee_name=task.assigned_to.username if task.assigned_to else 'Unassigned'
        tasks_with_assignee.append({
            'task':task,
            'assignee_name':assignee_name
        })
    
    return render(request=request,template_name='project_flow/project_detail.html',context={'project':project,'members_usernames':member_usernames})


@login_required
def project_create(request):
    if request.method=='POST':
        title=request.POST.get('title')
        description=request.POST.get('description')
        start_date=request.POST.get('start_date')
        end_date=request.POST.get('end_date')
        status=request.POST.get('status')
        priority=request.POST.get('priority')
        member_ids=request.POST.getlist('members')

        project=Project.objects.create(
            title=title,
            description=description,
            start_date=start_date,
            end_date=end_date,
            status=status,
            priority=priority,          
            )
        if member_ids:            
            users=User.objects.filter(id__in=member_ids)
            project.members.set(users)
        return redirect('project_detail',pk=project.pk)
    users=User.objects.all()
    STATUS_CHOICES = [('todo', 'To Do'), ('work_in_progress', 'In Progress'), ('complete', 'Completed'),('on_hold','On Hold')]
    PRIORITY_CHOICES = [('low', 'Low'), ('medium', 'Medium'), ('high', 'High')]

    return render(request,'project_flow/project_form.html',{
        'users':users,
        'status_choices':STATUS_CHOICES,
        'priority_choices':PRIORITY_CHOICES,
    })


@login_required
def project_update(request,pk):
    project=get_object_or_404(Project,pk=pk)
    if request.method=='POST':
        project.title=request.POST.get('title')
        project.description=request.POST.get('description')
        project.start_date=request.POST.get('start_date')
        project.end_date=request.POST.get('end_date')
        project.status=request.POST.get('status')
        project.priority=request.POST.get('priority')
        member_ids=request.POST.getlist('members')

        
        if member_ids:            
            users=User.objects.filter(id__in=member_ids)
            project.members.set(users)
        else:
            project.members.clear()
        project.save()
        return redirect('project_detail',pk=project.pk)
    users=User.objects.all()
    STATUS_CHOICES = [('todo', 'To Do'), ('work_in_progress', 'In Progress'), ('complete', 'Completed'),('on_hold','On Hold')]
    PRIORITY_CHOICES = [('low', 'Low'), ('medium', 'Medium'), ('high', 'High')]

    return render(request,'project_flow/project_form.html',{
        'users':users,
        'status_choices':STATUS_CHOICES,
        'priority_choices':PRIORITY_CHOICES,
        'project':project,
    })


@login_required
def project_delete(request,pk):
    project=get_object_or_404(Project,pk=pk)
    if request.method=='POST':
        project.delete()
        return redirect('dashboard')
    return render(request,'project_flow\project_confirm_delete.html',context={'project':project})


# View 1: Task List (for a specific project)
@login_required
def task_list(request, project_id):
    try:
        project = get_object_or_404(Project, id=project_id)
    except Project.DoesNotExist:
        raise Http404("Project not found")

    tasks = project.tasks.all()  # Fixed: 'al1()' → 'all()'

    print(f"Project ID: {project_id}")
    print(f"Tasks for project: {tasks}")

    return render(request, r'project_flow\task_list.html', {
        'project': project,
        'tasks': tasks
    })

# View 2: Task Detail (for a specific task)
@login_required
def task_detail(request, pk):
    try:
        task = get_object_or_404(Task, pk=pk)
    except Task.DoesNotExist:
        raise Http404("Task not found")

    print(f"Task ID: {pk}")

    return render(request, 'project_flow/task_detail.html', {
        'task': task
    })


@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if request.method == 'POST':
        # Get the project ID
        project_id = task.project.pk
        task.delete()
        # Redirect to task list for that project
        return redirect('task_list', project_id=project_id)

    # If GET request, show confirmation page
    return render(request, 'project_flow/task_confirm_delete.html', {
        'task': task
    })

# View 2: User Projects (projects assigned to user)
@login_required
def user_projects(request):
    projects = Project.objects.filter(members=request.user).order_by("status", "-start_date").distinct()

    return render(request, 'project_flow/project_list.html', {
        'projects': projects
    })



@login_required
def user_tasks(request):
    # Fetch tasks assigned to the current user
    tasks = Task.objects.filter(assigned_to=request.user).select_related("project").order_by("due_date", "-priority")

    # Optional: Debug print (remove in production)
    # print(f"Tasks assigned to {request.user}: {tasks}")

    return render(request, "project_flow/user_task_list.html", {
        "tasks": tasks
    })

@login_required
def task_create(request,project_id):
    project=get_object_or_404(Project,pk=project_id)
    PRIORITY_CHOICES = [('low', 'Low'), ('medium', 'Medium'), ('high', 'High')]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    if request.method=='POST':
        title=request.POST.get('title')
        description=request.POST.get('description')
        status=request.POST.get('status')
        priority=request.POST.get('priority')
        due_date=request.POST.get('due_date')
        assigned_to_id=request.POST.get('assigned_to')

        assigned_to=User.objects.filter(id=assigned_to_id).first() if assigned_to_id else None

        task=Task.objects.create(
            project=project,
            title=title,
            description=description,
            status=status,
            priority=priority,
            due_date=due_date,
            assigned_to=assigned_to
        )
        return redirect('task_detail',pk=task.pk)
    users=User.objects.all()
    return render(request,'project_flow/task_form.html',{'project':project,'users':users,'status_choices':STATUS_CHOICES,'priority_choices':PRIORITY_CHOICES})



def task_update(request,pk):
    task=get_object_or_404(Task,pk=pk)
    if request.method=='POST':
        task.title=request.POST.get('title')
        task.description=request.POST.get('description')
        task.status=request.POST.get('status')
        task.priority=request.POST.get('priority')
        task.due_date=request.POST.get('due_date')
        assigned_to_id=request.POST.get('assigned_to')

        task.assigned_to=User.objects.filter(id=assigned_to_id).first() if assigned_to_id else None

        task.save()
        return redirect('task_detail',pk=task.pk)
    users=User.objects.all()
    project=task.project
    status_choices=Task.STATUS_CHOICES
    priority_choices=Task.PRIORITY_CHOICES
    context={
        'task':task,
        'project':project,
        'users':users,
        'status_choices':status_choices,
        'priority_choices':priority_choices
    }
    return render(request,'project_flow/task_form.html',context)


