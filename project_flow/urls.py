from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('dashboard',view=views.dashboard,name='dashboard'),
    path('project/add/', views.add_project, name='add_project'),
    path('project/<int:pk>/', views.project_detail, name='project_detail'),
    path('project/<int:project_id>/task/add/', views.add_task, name='add_task'),
    path('project/<int:project_id>/document/add/', views.add_document, name='add_document'),
    path('task/<int:task_id>/comment/add/', views.add_comment, name='add_comment'),
]
