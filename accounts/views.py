from django.shortcuts import render

# Create your views here.

# accounts/views.py
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic


from django.contrib.auth.models import User

class UserCreationForm_email(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email")


class SignUp(generic.CreateView):
    form_class = UserCreationForm_email
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
