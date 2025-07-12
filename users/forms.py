from attr import fields
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import User

User = get_user_model() #Return the user model that is active in this project.

class RegisterMemberForm (UserCreationForm):
    class Meta:
        model=User
        # fields=['email','username']
        fields = ['username', 'email', 'role', 'password1', 'password2']


    def clean_email(self):
        email=self.cleaned_data.get('email')

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("This email address is already in use. Please use a different email")
