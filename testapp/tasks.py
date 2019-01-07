from __future__ import absolute_import

from celery import shared_task

@shared_task
def test(param):
    return 'The test task executed with argument "%s" ' % param

@shared_task
def test2(param):
    return 'test2: "%s"' % param


import subprocess
import webapp.settings as SETTING
import os
import sys

@shared_task
def runSample(sample):
    sample_file = str(sample.file)

    sample_dir_path = os.path.join(SETTING.MEDIA_ROOT, "/".join(sample_file.split("/")[:-1]))

    filename_contig = sample_file.split("/")[-1]
    filename_prod = filename_contig + ".prodigal.fa"
    filename_prod_log = filename_contig + ".prodigal.fa.log"


    filepath_contig = os.path.join(sample_dir_path, filename_contig)
    filepath_prod = os.path.join(sample_dir_path, filename_prod)
    filepath_prod_log = os.path.join(sample_dir_path, filename_prod_log)

    filepath_output = os.path.join(sample_dir_path, "out.txt")


    subprocess.call(["prodigal", "-i", filepath_contig, "-d", filepath_prod, "-p", "meta", "-o", filepath_prod_log])

    subprocess.call(["which", "python3"])
    subprocess.call(["python3", "--version"])

    #sys.path.append("/home/minoh/anaconda3/bin")
    print(sys.path)

    #subprocess.call(["python3", "/home/minoh/MetaCompare2_cmd/metacmp2.py", "-c", filepath_contig, "-g", filepath_prod, "-o", sample_dir_path])
    subprocess.Popen(["python", "/home/minoh/MetaCompare2_cmd/metacmp2.py", "-c", filepath_contig, "-g", filepath_prod, "-o", sample_dir_path],
                     env={'PYTHONPATH': "/home/minoh/anaconda3/bin",
                          'PATH': "/home/minoh/anaconda3/bin"})
                     #env = {'PYTHONPATH': os.pathsep.join(sys.path), 'PATH': os.pathsep.join(["/home/minoh/anaconda3/bin"])})

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
        sample.qARG = float(vals['fARG'])
        sample.qARG_MGE = float(vals['fARG_MGE'])
        sample.qARG_MGE_PAT = float(vals['fARG_MGE_PAT'])
        sample.risk_score = float(vals['score'])
        sample.stat = 2
        sample.save()

    return 'done'




