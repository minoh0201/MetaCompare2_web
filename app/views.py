from django.shortcuts import render
from .models import Project
from .models import Sample

# Create your views here.

def main(request):
    return render(request, 'app/main.html', {})