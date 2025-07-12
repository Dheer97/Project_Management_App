from django.http import HttpResponse
from django.utils.html import escape
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .forms import RegisterMemberForm
from django.utils.safestring import mark_safe
from django.views.decorators.http import require_GET,require_POST,require_safe,require_http_methods
# Create your views here.

def register_member_view(request):
    form=RegisterMemberForm()
    context={'form':form}
    return render(request=request,template_name=r'users/register_users.html',context=context)

def register_member(request):
    if request.method=='POST':
        form=RegisterMemberForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request=request,message='Account Registration Successful.')
            print(messages)
            return redirect('view_login_page')
        else:
            msg="Account Registration Unsuccessful"
            # msg=''
            # if form.errors:
            #     error_dict={key:[mark_safe(error) for error in value] for key,value in form.errors.items()}
            #     err_list=[]
            #     for key,value in error_dict.items():
            #         err_list.append(''.join(value))
            #     msg=''.join(err_list)
            # messages.warning(request=request,message=msg)
            print(msg)
            return render(request=request,template_name=r'users/register_users.html',context={'form':form})
        
def login_user_view(request):
    return render(request,'users/login.html')

def login_user(request):
    if request.method=="POST":
        username=request.POST.get("username")
        password=request.POST.get("password")
        # print(username,password)
        user=authenticate(request,username=username,password=password)
        if user is not None and user.is_active:

            login (request, user)
            print('login successful')
            messages.info(request, 'Login successfull. Please enjoy your session')
            return redirect('dashboard')
        else:
            messages.warning(request, 'Something went wrong. Please check form input')
            return redirect("view_login_page")
    


