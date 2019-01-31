from django.db import models
from django.utils import timezone

from django.db.models.signals import post_delete
from django.dispatch import receiver

import os

from pathlib import Path

# Create your models here.

def user_project_path(instance):
    return 'data/{0}/{1}'.format(instance.user.username, instance.project.name)

class Project(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    #description = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    dir_path = models.FileField(upload_to=user_project_path, default='', blank=True)

    def publish(self):
        self.save()

    def __str__(self):
        return self.name

    def clean(self):
        if self.name:
            self.name = self.name.strip().replace(' ', '')

    def save(self, *args, **kwargs):
        self.full_clean() # performs regular validation then clean()
        # save directory path
        self.dir_path = 'data/{0}/{1}'.format(self.user.username, self.name)
        # save
        super(Project, self).save(*args, **kwargs)


def user_directory_path(instance, filename):
    os.path.join("")
    return 'data/{0}/{1}/{2}/{3}'.format(instance.user.username, instance.project.name, instance.name, filename)

# def user_directory_path_upper(instance, filename):
#     os.path.join("")
#     return 'data/{0}/{1}/{2}'.format(instance.user.username, instance.project.name, instance.name)

class Sample(models.Model):

    #properties of a sample
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    project = models.ForeignKey(Project, related_name='samples', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    #description = models.TextField(default='')
    file = models.FileField(upload_to=user_directory_path, default='')
    directory = models.FileField(default='', blank=True)
    created_date = models.DateTimeField(default=timezone.now)

    #technical values of a sample
    nContigs = models.IntegerField(default=0)
    nARG = models.IntegerField(default=0)
    nMGE = models.IntegerField(default=0)
    nPAT = models.IntegerField(default=0)

    qARG = models.FloatField(default=0.0)
    qARG_MGE = models.FloatField(default=0.0)
    qARG_MGE_PAT = models.FloatField(default=0.0)
    risk_score = models.FloatField(default=0.0)

    #Run status
    stat = models.IntegerField(default=0)


    def publish(self):
        self.save()

    def __str__(self):
        return self.name

    def clean(self):
        if self.name:
            self.name = self.name.strip().replace(' ', '')

    def save(self, *args, **kwargs):
        self.full_clean()  # performs regular validation then clean()
        self.directory = 'data/{0}/{1}/{2}'.format(self.user.username, self.project.name, self.name)
        super(Sample, self).save(*args, **kwargs)

@receiver(post_delete, sender=Sample)
def sample_delete(sender, instance, **kwargs):
    instance.file.delete(False)
    instance.directory.delete(False)

@receiver(post_delete, sender=Project)
def project_delete(sender, instance, **kwargs):
    instance.dir_path.delete(False)

#upload test
class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description

