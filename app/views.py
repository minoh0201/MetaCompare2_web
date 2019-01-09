from django.shortcuts import render
from django.shortcuts import redirect
from .models import Project
from .models import Sample

from django.contrib.auth.decorators import login_required

from .form import DocumentForm
from .form import SampleForm
from .form import ProjectForm

# Create your views here.

def main(request):
    return render(request, 'app/main.html', {})

#upload
from django.conf import settings
from django.core.files.storage import FileSystemStorage

#get object

from django.shortcuts import get_object_or_404

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
        form = SampleForm(request.user.id, request.POST, request.FILES)
        if form.is_valid():
            f_saver = form.save(commit=False)
            f_saver.user = request.user
            f_saver.save()
            return redirect('main')
    else:
        form = SampleForm(request.user.id)
    return render(request, 'app/sample_form_upload.html', {'form': form})


from django.forms import formset_factory
#from app.form import SampleForm
from django.views import View

@login_required
def sample_form_upload2(request):
    Sample_FormSet = formset_factory(SampleForm)
    if request.method == 'POST':
        form = Sample_FormSet(request.POST, request.FILES, form_kwargs={'user_id': request.user.id})
        if form.is_valid():
            for sample in form:
                s_saver = sample.save(commit=False)
                s_saver.user = request.user
                s_saver.save()
            return redirect('project')
    else:
        form = Sample_FormSet(form_kwargs={'user_id': request.user.id})
    return render(request, 'app/upload.html', {'sample_form': form})



@login_required
def my_project(request):
    projects = Project.objects.filter(user_id = request.user.id)
    samples = Sample.objects.filter(user_id = request.user.id)
    for sample in samples:
        # if sample is in running stage
        if sample.stat == 1:
            # get path to the result file
            sample_file = str(sample.file)
            sample_dir_path = os.path.join(SETTING.MEDIA_ROOT, "/".join(sample_file.split("/")[:-1]))
            filepath_output = os.path.join(sample_dir_path, "out.txt")
            # if result file exists, copy results to the sample instance
            if os.path.isfile(filepath_output):
                with open(filepath_output, "r") as f:
                    res = f.readlines()[0].split(',')
                    vals = {"nContigs": res[0], "nARG": res[1], "nMGE": res[2], "nPAT": res[3],
                            "nARG_MGE": res[4], "nARG_MGE_PAT": res[5],
                            "fARG": res[6], "fMGE": res[7], "fPAT": res[8],
                            "fARG_MGE": res[9], "fARG_MGE_PAT": res[10],
                            "score": res[11],
                            }

                    sample.nContigs = int(vals['nContigs'])
                    sample.nARG = int(vals['nARG'])
                    sample.nMGE = int(vals['nMGE'])
                    sample.nPAT = int(vals['nPAT'])
                    sample.qARG = float(format(float(vals['fARG']), '.8f'))
                    sample.qARG_MGE = float(format(float(vals['fARG_MGE']), '.8f'))
                    sample.qARG_MGE_PAT = float(format(float(vals['fARG_MGE_PAT']), '.8f'))
                    sample.risk_score = float(format(float(vals['score']), '.2f'))
                    sample.stat = 2
                    sample.save()

    return render(request, 'app/project.html', {'projects': projects})#, 'samples': samples})

from testapp.tasks import runSample
import webapp.settings as SETTING
import os

@login_required
def run(request, pk):

    sample = get_object_or_404(Sample, pk=pk)
    sample.stat = 1
    sample.save()

    #queue: testapp.tasks (see tasks.py)
    runSample.delay(str(sample.file))

    return redirect('project')


@login_required
def add_project(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('project')
    else:
        form = ProjectForm()
    return render(request, 'app/add_project.html', {'form': form})



    # if request.method == 'POST':
    #     form = Sample_FormSet(request.POST, request.FILES, form_kwargs={'user_id': request.user.id})
    #     if form.is_valid():
    #         for sample in form:
    #             s_saver = sample.save(commit=False)
    #             s_saver.user = request.user
    #             s_saver.save()
    #         return redirect('project')
    # else:
    #     form = Sample_FormSet(form_kwargs={'user_id': request.user.id})
