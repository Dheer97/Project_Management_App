from django import forms
from .models import Project, Task, Document, Comment





class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'title',
            'description',
            'start_date',
            'end_date',
            'status',
            'priority',
            'members'
        ]
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'status': forms.Select(),
            'priority': forms.Select(),
            'members': forms.SelectMultiple()
        }

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            # 'project',
            'title',
            'description',
            'status',
            'priority',
            'due_date',
            'assigned_to'
        ]
        widgets = {
            # 'project': forms.Select(),
            'status': forms.Select(),
            'priority': forms.Select(),
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'assigned_to': forms.Select()
        }



class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = [
            'project',
            'name',
            'version',
            'path',
            'uploaded_by'
        ]
        widgets = {
            'project': forms.Select(),
            'uploaded_by': forms.Select()
        }




class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'task',
            'document',
            'content',
            'created_by'
        ]
        widgets = {
            'task': forms.Select(),
            'document': forms.Select(),
            'created_by': forms.Select()
        }
