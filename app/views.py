from django.shortcuts import render
from django.shortcuts import redirect
from .models import Project
from .models import Sample

from django.contrib.auth.decorators import login_required

from .form import DocumentForm
from .form import SampleForm
from .form import ProjectForm

import math


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
            if os.path.isfile(filepath_output) & os.path.isfile(os.path.join(sample_dir_path,"pa_result.csv")):
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
                    sample.qARG = qARG = float(format(float(vals['fARG']), '.8f'))
                    sample.qARG_MGE = qARG_MGE = float(format(float(vals['fARG_MGE']), '.8f'))
                    sample.qARG_MGE_PAT = qARG_MGE_PAT = float(format(float(vals['fARG_MGE_PAT']), '.8f'))

                    # check validity of risk score by calculating distance and observing whether it is less than 0.01
                    dist = math.sqrt((0.01-qARG)**2 + (0.01-qARG_MGE)**2 + (0.01-qARG_MGE_PAT)**2)
                    if dist <= 0.01:
                        sample.risk_score = 0.0001
                    else:
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
def run_all(request, pk):
    samples = Sample.objects.filter(project=pk)
    for sample in samples:
        if sample.stat == 0:
            sample.stat = 1
            sample.save()

            # queue: testapp.tasks (see tasks.py)
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

import csv
from django.http import HttpResponse

@login_required
def export_project_csv(request, pk):
    project = get_object_or_404(Project, pk=pk)
    samples = Sample.objects.filter(project=pk)

    response = HttpResponse(content_type='text/csv')

    response['Content-Disposition'] = 'attachment; filename=' + project.name + '.csv'

    writer = csv.writer(response)
    writer.writerow(['Sample_name', '#Contigs', '#ARG', '#MGE', '#PAT', '#Q(ARG)', '#Q(ARG_MGE)', '#Q(ARG_MGE_PAT)', 'Risk_Score'])

    for sample in samples:
        # check if it is immeasurable or not
        if sample.risk_score == 0.0001:
            risk_score = 'Immeasurable'
        else:
            risk_score = sample.risk_score

        # print(sample, sample.nContigs, sample.nARG, sample.nMGE, sample.nPAT, sample.qARG, sample.qARG_MGE, sample.qARG_MGE_PAT, sample.risk_score)
        row = [sample, sample.nContigs, sample.nARG, sample.nMGE, sample.nPAT, sample.qARG, sample.qARG_MGE,
               sample.qARG_MGE_PAT, risk_score]
        writer.writerow([str(x) for x in row])

    return response


@login_required
def sample_remove(request, pk):
    sample = get_object_or_404(Sample, pk=pk)
    sample.delete()
    return redirect('project')

@login_required
def project_remove(request, pk):
    project = get_object_or_404(Project, pk=pk)
    project.delete()
    return redirect('project')

import pandas as pd
import numpy as np
import operator

from Bio import SeqIO
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render

@login_required
def display_all_scaffolds(request, pk):

    sample = get_object_or_404(Sample, pk=pk)
    sample_file = str(sample.file)
    sample_file = os.path.join(SETTING.MEDIA_ROOT, sample_file)

    # Get scaffold list from samples file uploaded by user
    scaffold_list_unsorted = SeqIO.parse(sample_file, "fasta")

    # Sort descending by length of scaffolds
    scaffold_list = sorted(list(scaffold_list_unsorted),
                            key=lambda a: len(a),
                            reverse=True)

    # Pagination Code
    page = request.GET.get('page',1)
    paginator = Paginator(scaffold_list, 20)
    try:
        scaffolds = paginator.page(page)
    except PageNotAnInteger:
        scaffolds = paginator.page(1)
    except EmptyPage:
        scaffolds = paginator.page(paginator.num_pages)


    # Get scaffold list from samples file uploaded by user
    scaffold_indexed = SeqIO.to_dict(SeqIO.parse(sample_file, "fasta"))

    # Get best hits
    sample_file = str(sample.file)
    sample_dir_path = os.path.join(SETTING.MEDIA_ROOT, "/".join(sample_file.split("/")[:-1]))
    ac_file = os.path.join(sample_dir_path, 'ac_result.csv')
    ca_file = os.path.join(sample_dir_path, 'ca_result.csv')
    pa_file = os.path.join(sample_dir_path, 'pa_result.csv')
    if not os.path.exists(ac_file):
        return redirect('run', pk=pk)
    ac = pd.read_csv(ac_file, index_col=0)
    ca = pd.read_csv(ca_file, index_col=0)
    pa = pd.read_csv(pa_file, index_col=0)
    
    # Get scaffolds having all 3 - ARGs, MGEs, PATHOGENs
    scaffold_intscn = np.intersect1d(ca.scaffold_id, np.intersect1d(ac.scaffold_id, pa.scaffold_id)).tolist()

    return render(request, 'app/display_scaffolds.html', {'scaffolds': scaffolds, 'pk': pk, 'all': 1, 'scaffold_intscn': scaffold_intscn})

@login_required
def display_scaffolds(request, pk):

    sample = get_object_or_404(Sample, pk=pk)
    sample_file = str(sample.file)
    sample_file = os.path.join(SETTING.MEDIA_ROOT, sample_file)

    # Get scaffold list from samples file uploaded by user
    scaffold_indexed = SeqIO.to_dict(SeqIO.parse(sample_file, "fasta"))

    # Get best hits
    sample_file = str(sample.file)
    sample_dir_path = os.path.join(SETTING.MEDIA_ROOT, "/".join(sample_file.split("/")[:-1]))
    ac_file = os.path.join(sample_dir_path, 'ac_result.csv')
    ca_file = os.path.join(sample_dir_path, 'ca_result.csv')
    pa_file = os.path.join(sample_dir_path, 'pa_result.csv')
    if not os.path.exists(ac_file):
        return redirect('run', pk=pk)
    ac = pd.read_csv(ac_file, index_col=0)
    ca = pd.read_csv(ca_file, index_col=0)
    pa = pd.read_csv(pa_file, index_col=0)
    
    # Get scaffolds having all 3 - ARGs, MGEs, PATHOGENs
    scaffold_intscn = np.intersect1d(ca.scaffold_id, np.intersect1d(ac.scaffold_id, pa.scaffold_id)).tolist()  
    common_scaffolds = [scaffold_indexed.get(key) for key in scaffold_intscn]

    # Sort descending by length of scaffolds
    common_scaffolds = sorted(common_scaffolds, key = len, reverse=True)

    page = request.GET.get('page',1)
    paginator = Paginator(common_scaffolds, 20)
    try:
        scaffolds = paginator.page(page)
    except PageNotAnInteger:
        scaffolds = paginator.page(1)
    except EmptyPage:
        scaffolds = paginator.page(paginator.num_pages)
        
    return render(request, 'app/display_scaffolds.html', {'scaffolds': scaffolds, 'pk': pk, 'scaffold_intscn': scaffold_intscn})

@login_required
def visualize_scaffold(request, pk, scaffold_id, length, sequence):

    sample = get_object_or_404(Sample, pk=pk)
    sample_file = str(sample.file)
    sample_dir_path = os.path.join(SETTING.MEDIA_ROOT, "/".join(sample_file.split("/")[:-1]))
    
    ac_file = os.path.join(sample_dir_path, 'ac_result.csv')
    ca_file = os.path.join(sample_dir_path, 'ca_result.csv')
    pa_file = os.path.join(sample_dir_path, 'pa_result.csv')

    ac = pd.read_csv(ac_file, index_col=0)
    ac = ac.loc[ac['scaffold_id'] == scaffold_id]

    ca = pd.read_csv(ca_file, index_col=0)
    ca = ca.loc[ca['scaffold_id'] == scaffold_id]

    pa = pd.read_csv(pa_file, index_col=0)
    pa = pa.loc[pa['scaffold_id'] == scaffold_id]


    def get_dict(row,group):
        if isinstance(row['sub_id'],float):
            content = 'null'
        else:
            content = row['sub_id']
        if group == 1:
            class_name = 'arg'
            js_id = 'arg'+str(itr)
        elif group == 2:
            class_name = 'mge'
            js_id = 'mge'+str(itr)
        else:
            class_name = 'pat'
            js_id = 'pat'+str(itr)
        start = row['qStart']
        end = row['qEnd']

        return {'id': js_id, 'group': group, 'content': content, 'className': class_name, 'start': start, 'end': end}

    def get_hit(row,_type):
        _type = _type
        _id = row['sub_id']
        start = row['qStart']
        end = row['qEnd']
        _sequence = sequence[start-1:end-1]

        return {'id':_id, 'type':_type, 'start':start, 'end':end, "sequence":_sequence}
        
    data_set = []
    hits = []

    itr = 1
    data_set.append({'id': 'arg0', 'group': 1, 'content': "", 'className': 'arg', 'start': -1, 'end': -1})
    for idx, row in ca.iterrows():
        data_set.append(get_dict(row,1))
        hits.append(get_hit(row,"ARG"))
        itr += 1
    data_set.append({'id': 'arg'+str(itr), 'group': 1, 'content': "", 'className': 'arg', 'start': length, 'end': length})

    itr = 1
    data_set.append({'id': 'mge0', 'group': 2, 'content': "", 'className': 'mge', 'start': -1, 'end': -1})
    for idx, row in ac.iterrows():
        data_set.append(get_dict(row,2))
        hits.append(get_hit(row,"MGE"))
        itr += 1
    data_set.append({'id': 'mge'+str(itr), 'group': 2, 'content': "", 'className': 'mgr', 'start': length, 'end': length})
    
    itr = 1
    data_set.append({'id': 'pat0', 'group': 3, 'content': "", 'className': 'pat', 'start': -1, 'end': -1})
    for idx, row in pa.iterrows():
        data_set.append(get_dict(row,3))
        hits.append(get_hit(row,"PATHOGEN"))
        itr += 1
    data_set.append({'id': 'pat'+str(itr), 'group': 3, 'content': "", 'className': 'pat', 'start': length, 'end': length})
    
    data_set.append({'id': 'sequence', 'group': 0, 'content': scaffold_id, 'className': 'sequence', 'start': 1, 'end': length})
    
    return render(request, 'app/visualize_scaffold.html', {'pk':pk, 'data_set': data_set, 'length': length, 'sequence': sequence, 'scaffold_id': scaffold_id, 'hits':hits})