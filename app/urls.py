from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    #path('upload/', views.sample_form_upload, name='upload'),
    #path('upload/', views.uploadFormView.as_view(), name='upload'),

    path('upload/', views.sample_form_upload2, name='upload'),
    path('project/', views.my_project, name='project'),
    path('add_project/', views.add_project, name='add_project'),
    path('run/<int:pk>/', views.run, name='run'),
    path('run_all/<int:pk>/', views.run_all, name='run_all'),
    path('export_csv/<int:pk>/', views.export_project_csv, name='export_csv'),
    path('project_remove/<int:pk>/', views.project_remove, name='project_remove'),
    path('sample_remove/<int:pk>/', views.sample_remove, name='sample_remove'),
    path('visualize_scaffold/<int:pk>/<str:scaffold_id>/<int:length>/<str:sequence>', views.visualize_scaffold, name='visualize_scaffold'),
    path('display_scaffolds/<int:pk>', views.display_scaffolds, name='display_scaffolds'),
    path('display_all_scaffolds/<int:pk>', views.display_all_scaffolds, name='display_all_scaffolds'),
    path('confirm_run/<int:pk>', views.confirm_run, name='confirm_run'),
    path('how_to', views.how_to, name='how_to'),
]