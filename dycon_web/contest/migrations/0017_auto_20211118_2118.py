# Generated by Django 3.2.7 on 2021-11-18 21:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0016_auto_20211118_2113'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompetitionSubmissionStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stat', models.CharField(choices=[('submitting', 'submitting'), ('submitted', 'submitted'), ('running', 'running'), ('failed', 'failed'), ('cancelled', 'cancelled'), ('finished', 'finished'), ('None', 'None')], default='None', max_length=64)),
            ],
        ),
        migrations.AddField(
            model_name='competitionsubmission',
            name='coopetition_file',
            field=models.FileField(blank=True, null=True, upload_to='submission_coopetition'),
        ),
        migrations.AddField(
            model_name='competitionsubmission',
            name='detailed_results_file',
            field=models.FileField(blank=True, null=True, upload_to='submission_detailed_results'),
        ),
        migrations.AddField(
            model_name='competitionsubmission',
            name='history_file',
            field=models.FileField(blank=True, null=True, upload_to='submission_history'),
        ),
        migrations.AddField(
            model_name='competitionsubmission',
            name='prediction_stderr_file',
            field=models.FileField(blank=True, null=True, upload_to='predict_submission_stderr'),
        ),
        migrations.AddField(
            model_name='competitionsubmission',
            name='prediction_stdout_file',
            field=models.FileField(blank=True, null=True, upload_to='predict_submission_stdout'),
        ),
        migrations.AddField(
            model_name='competitionsubmission',
            name='private_output_file',
            field=models.FileField(blank=True, null=True, upload_to='submission_private_output'),
        ),
        migrations.AddField(
            model_name='competitionsubmission',
            name='runfile',
            field=models.FileField(blank=True, null=True, upload_to='submission_runfile'),
        ),
        migrations.AddField(
            model_name='competitionsubmission',
            name='status_details',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='competitionsubmission',
            name='status',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='contest.competitionsubmissionstatus'),
        ),
    ]
