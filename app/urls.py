from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    #path('upload/', views.sample_form_upload, name='upload'),
    #path('upload/', views.uploadFormView.as_view(), name='upload'),

    path('upload/', views.sample_form_upload2, name='upload'),
    path('project/', views.my_project, name='project'),
]