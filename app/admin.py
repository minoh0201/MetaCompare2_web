from django.contrib import admin
from .models import Project
from .models import Sample
from .models import Document

# Register your models here.

admin.site.register(Project)
admin.site.register(Sample)
admin.site.register(Document)