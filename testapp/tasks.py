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

@shared_task
def runSample(sample_file):

    sample_dir_path = os.path.join(SETTING.MEDIA_ROOT, "/".join(sample_file.split("/")[:-1]))

    filename_contig = sample_file.split("/")[-1]
    filename_prod = filename_contig + ".prodigal.fa"
    filename_prod_log = filename_contig + ".prodigal.fa.log"
    filepath_output = os.path.join(sample_dir_path, "out.txt")

    filepath_contig = os.path.join(sample_dir_path, filename_contig)
    filepath_prod = os.path.join(sample_dir_path, filename_prod)
    filepath_prod_log = os.path.join(sample_dir_path, filename_prod_log)

    #if output is already exist then remove old output
    if os.path.isfile(filepath_output):
        subprocess.call(["rm", "-f", filepath_output])


    #run prodigal
    if not os.path.isfile(filepath_prod):
        subprocess.call(["prodigal", "-i", filepath_contig, "-d", filepath_prod, "-p", "meta", "-o", filepath_prod_log])

    #run MetaCompare2
    subprocess.Popen(["python", "/home/minoh/MetaCompare2_cmd/metacmp2.py", "-c", filepath_contig, "-g", filepath_prod, "-o", sample_dir_path],
                     env={'PYTHONPATH': "/home/minoh/anaconda3/bin",
                          'PATH': "/home/minoh/anaconda3/bin"})

    return 'done'




