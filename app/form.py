from django import forms
from .models import Document
from .models import Sample

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('description', 'document', )

class SampleForm(forms.ModelForm):
    class Meta:
        model = Sample
        fields = ('user', 'project', 'name', 'description', 'file', )