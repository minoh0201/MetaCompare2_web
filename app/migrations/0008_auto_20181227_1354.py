# Generated by Django 2.1.2 on 2018-12-27 18:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20181227_1349'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sample',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='samples', to='app.Project'),
        ),
    ]
