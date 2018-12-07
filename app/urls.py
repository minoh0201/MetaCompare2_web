from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('upload/', views.sample_form_upload, name='upload')
]