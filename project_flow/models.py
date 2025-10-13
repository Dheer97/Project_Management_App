from tabnanny import verbose
from django.db import models
from users.models import User


class Project(models.Model):
    STATUS_CHOICES = [('todo', 'To Do'), ('work_in_progress', 'In Progress'), ('complete', 'Completed'),('on_hold','On Hold')]
    PRIORITY_CHOICES = [('low', 'Low'), ('medium', 'Medium'), ('high', 'High')]
    
    title = models.CharField(max_length=255,verbose_name='Project Name')
    description = models.TextField(verbose_name='Project Description')
    start_date = models.DateField(verbose_name='Project Start Date')
    end_date = models.DateField(verbose_name='Project End Date')
    status = models.CharField(max_length=50,choices=STATUS_CHOICES,verbose_name='Project Status')
    priority=models.CharField(max_length=10, choices=PRIORITY_CHOICES,verbose_name='Project Priority')
    members = models.ManyToManyField(User, related_name='projects',verbose_name='Project Members')

    def _str_(self):
        return self.title

class Task(models.Model):
    PRIORITY_CHOICES = [('low', 'Low'), ('medium', 'Medium'), ('high', 'High')]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=255,verbose_name='Task Name')
    description = models.TextField(verbose_name='Task Description')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES,verbose_name='Task Status',default='pending')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES,verbose_name='Task Priority')
    due_date = models.DateField(verbose_name='Due Date')
    created_at = models.DateTimeField(auto_now_add=True)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks',verbose_name='Assigned To')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.project.title

class Document(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='documents')
    name = models.CharField(max_length=255)
    version = models.CharField(max_length=50)
    path = models.FileField(upload_to='documents/')
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments', null=True, blank=True)
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='comments', null=True, blank=True)
    content = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
