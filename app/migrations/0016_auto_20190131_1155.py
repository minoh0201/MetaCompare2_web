# Generated by Django 2.1.2 on 2019-01-31 16:55

import app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_auto_20190131_1148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='dir_path',
            field=models.FileField(default='', upload_to=app.models.user_project_path),
        ),
    ]
