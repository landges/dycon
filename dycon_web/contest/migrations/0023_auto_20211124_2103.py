# Generated by Django 3.2.7 on 2021-11-24 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0022_pagecompetition'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='competition',
            name='image_url_base',
        ),
        migrations.AlterField(
            model_name='competitionsubmission',
            name='inputfile',
            field=models.FileField(blank=True, null=True, upload_to='submission_inputfile/%Y%m%d/%h%m%s/'),
        ),
    ]