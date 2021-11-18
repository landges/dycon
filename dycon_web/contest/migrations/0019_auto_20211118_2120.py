# Generated by Django 3.2.7 on 2021-11-18 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0018_auto_20211118_2120'),
    ]

    operations = [
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
            name='prediction_output_file',
            field=models.FileField(blank=True, null=True, upload_to='submission_prediction_output'),
        ),
        migrations.AddField(
            model_name='competitionsubmission',
            name='prediction_runfile',
            field=models.FileField(blank=True, null=True, upload_to='submission_prediction_runfile'),
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
            name='scores_file',
            field=models.FileField(blank=True, null=True, upload_to='submission_scores'),
        ),
        migrations.AddField(
            model_name='competitionsubmission',
            name='status_details',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='competitionsubmission',
            name='stderr_file',
            field=models.FileField(blank=True, null=True, upload_to='submission_stderr'),
        ),
        migrations.AddField(
            model_name='competitionsubmission',
            name='stdout_file',
            field=models.FileField(blank=True, null=True, upload_to='submission_stdout'),
        ),
    ]