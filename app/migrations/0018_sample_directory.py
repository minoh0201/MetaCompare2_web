# Generated by Django 2.1.2 on 2019-01-31 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_auto_20190131_1207'),
    ]

    operations = [
        migrations.AddField(
            model_name='sample',
            name='directory',
            field=models.FileField(blank=True, default='', upload_to=''),
        ),
    ]