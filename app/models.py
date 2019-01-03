from django.db import models
from django.utils import timezone

import os

from pathlib import Path

# Create your models here.

class Project(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    #description = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    def publish(self):
        self.save()

    def __str__(self):
        return self.name

    def clean(self):
        if self.name:
            self.name = self.name.strip().replace(' ', '')

    def save(self, *args, **kwargs):
        self.full_clean() # performs regular validation then clean()
        super(Project, self).save(*args, **kwargs)

def user_directory_path(instance, filename):
    os.path.join("")
    return 'data/{0}/{1}/{2}/{3}'.format(instance.user.username, instance.project.name, instance.name, filename)

class Sample(models.Model):

    #properties of a sample
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    project = models.ForeignKey(Project, related_name='samples', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    #description = models.TextField(default='')
    file = models.FileField(upload_to=user_directory_path, default='')
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
        super(Sample, self).save(*args, **kwargs)


#upload test
class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description

