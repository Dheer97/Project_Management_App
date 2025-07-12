from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('developer', 'Developer'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return self.username
    
    def save(self,*args,**kwargs):
        #Ensure the email is stored in lower case
        if self.email:
            self.email=self.email.lower()

        #Set last login to date joined if it is new user
        if not self.pk:
            self.last_login =self.date_joined

        super().save(*args,**kwargs)