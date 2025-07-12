from django import forms
from .models import Project, Task, Document, Comment





class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = '__all__'

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = '__all__'
