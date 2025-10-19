from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('dashboard/',views.project_list,name='dashboard'),
    path('projects/create',views.project_create,name='project_create'),
    path('projects/<int:pk>/',views.project_detail,name='project_detail'),
    path('projects/<int:pk>/edit/',views.project_update,name='project_update'),
    path('projects/<int:pk>/delete',views.project_delete,name='project_delete'),

    path('projects/<int:project_id>/tasks',views.task_list,name='task_list'),
    path('projects/<int:project_id>/tasks/create',views.task_create,name='task_create'),

    path('tasks/<int:pk>/',views.task_detail,name='task_detail'),
    path('tasks/<int:pk>/edit',views.task_update,name='task_update'),
    path('tasks/<int:pk>/delete',views.task_delete,name='task_delete'),

    path('projects/user_projects/',views.user_projects,name='user_projects'),
    path('projects/user_tasks/',views.user_tasks,name='user_tasks'),
    

    

]