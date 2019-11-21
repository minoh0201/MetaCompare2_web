# accounts/urls.py
from django.urls import path
from django.conf.urls import url

from . import views


urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('change_password/',views.change_password, name='change_password')
]