from django.shortcuts import render
from django.shortcuts import redirect
from .models import Project
from .models import Sample

from .form import DocumentForm
from .form import SampleForm

# Create your views here.

def main(request):
    return render(request, 'app/main.html', {})

#upload
from django.conf import settings
from django.core.files.storage import FileSystemStorage

def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render (request, 'app/simple_upload.html', {'uploaded_file_url': uploaded_file_url})
    return render(request, 'app/simple_upload.html')


def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('main')
    else:
        form = DocumentForm()
    return render(request, 'app/model_form_upload.html', {
        'form': form
    })

def sample_form_upload(request):
    if request.method == 'POST':
        form = SampleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('main')
    else:
        form = SampleForm()
    return render(request, 'app/sample_form_upload.html', {'form': form})

