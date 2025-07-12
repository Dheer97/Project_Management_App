from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register-member-view',view=views.register_member_view,name='register_member_view'),
    path('register-member/',view=views.register_member,name='register_member'),
    path('',view=views.login_user_view,name='view_login_page'),
    path('login/',view=views.login_user,name='login')
]
