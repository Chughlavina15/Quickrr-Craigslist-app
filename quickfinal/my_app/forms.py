#already defined the fields in your model
from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
#to store database of people filled the form
from django.contrib.auth.models import User


#from .models import Order

class CreateUserForm(UserCreationForm):
    class Meta:
        model=User
        # User is the name of database
        fields=['username','email','password2']
