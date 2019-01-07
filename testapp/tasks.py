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
def runSample(sample_file):

    sample_dir_path = os.path.join(SETTING.MEDIA_ROOT, "/".join(sample_file.split("/")[:-1]))

    filename_contig = sample_file.split("/")[-1]
    filename_prod = filename_contig + ".prodigal.fa"
    filename_prod_log = filename_contig + ".prodigal.fa.log"

    filepath_contig = os.path.join(sample_dir_path, filename_contig)
    filepath_prod = os.path.join(sample_dir_path, filename_prod)
    filepath_prod_log = os.path.join(sample_dir_path, filename_prod_log)

    subprocess.call(["prodigal", "-i", filepath_contig, "-d", filepath_prod, "-p", "meta", "-o", filepath_prod_log])

    subprocess.call(["which", "python3"])
    subprocess.call(["python3", "--version"])

    sys.path.append("/home/minoh/anaconda3/bin/diamond")
    print(sys.path)



    #subprocess.call(["python3", "/home/minoh/MetaCompare2_cmd/metacmp2.py", "-c", filepath_contig, "-g", filepath_prod, "-o", sample_dir_path])
    subprocess.Popen(["python3", "/home/minoh/MetaCompare2_cmd/metacmp2.py", "-c", filepath_contig, "-g", filepath_prod, "-o", sample_dir_path],
                     env = {'PYTHONPATH': os.pathsep.join(sys.path)})
    return 'done'




