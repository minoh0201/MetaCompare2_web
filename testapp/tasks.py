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

    filepath = os.path.join(SETTING.MEDIA_ROOT, sample_file)
    filename = sample_file.split("/")[-1]

    destpath = "/".join(sample_file.split("/")[:-1])
    destpath = os.path.join(destpath, filename + ".prodigal.fa")
    destpath = os.path.join(SETTING.MEDIA_ROOT, destpath)

    subprocess.call(["prodigal", "-i", filepath, "-d", destpath, "-p", "meta"])

    return 'done'




