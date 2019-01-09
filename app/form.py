from django import forms
from .models import Document
from .models import Sample, Project

from django.forms import formset_factory

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('description', 'document', )

class SampleForm(forms.ModelForm):
    def __init__(self, user_id, *args, **kwargs):
        super (SampleForm, self).__init__(*args, **kwargs)
        self.fields['project'].queryset = Project.objects.filter(user_id = user_id)
    class Meta:
        model = Sample
        fields = ('project', 'name', 'file', )
        labels = {
            'name': "Sample name"
        }

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('name',)
        labels = {
            'name': "Project name"
        }

