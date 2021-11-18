from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse
from datetime import datetime

# Dataset model
class Dataset(models.Model):
    """Model to create a dataset for a competition."""
    creator = models.ForeignKey(User, related_name='datasets',on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.TextField()
    number = models.PositiveIntegerField(default=1)
    datafile = models.FileField(upload_to='datasets')

    class Meta:
        ordering = ["number"]



class OrganizerDataSet(models.Model):
    TYPES = (
        ("Reference Data", "Reference Data"),
        ("Scoring Program", "Scoring Program"),
        ("Input Data", "Input Data"),
        ("Ingestion Program", "Ingestion Program"),
        ("Starting Kit", "Starting Kit"),
        ("Public Data", "Public Data"),
        ("None", "None")
    )
    name = models.CharField(max_length=255)
    full_name = models.TextField(default="")
    type = models.CharField(max_length=64, choices=TYPES, default="None")
    description = models.TextField(null=True, blank=True)
    data_file = models.FileField(
        upload_to='dataset_data_file',
        verbose_name="Data file",
        blank=True,
        null=True,
    )
    sub_data_files = models.ManyToManyField('OrganizerDataSet', null=True, blank=True, verbose_name="Bundle of data files")
    uploaded_by = models.ForeignKey(User,on_delete=models.DO_NOTHING)
 

# Create your models here.
class Competition(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    label = models.CharField(max_length=300,null=True, blank=True)
    url_redirect = models.URLField(null=True, blank=True, verbose_name="URL Redirect", help_text="(NOTE: You should not have Registration Required above checked if using URL redirection, because upon redirect participants will not be approved and unable to participate.)")
    image = models.FileField(upload_to='logos', null=True, blank=True, verbose_name="Logo")
    image_url_base = models.CharField(max_length=255)
    has_registration = models.BooleanField(default=False, verbose_name="Registration Required")
    start_date = models.DateTimeField(null=True, blank=True, verbose_name="Start Date (UTC)")
    end_date = models.DateTimeField(null=True, blank=True, verbose_name="End Date (UTC)")
    creator = models.ForeignKey(User, related_name='competitioninfo_creator',on_delete=models.CASCADE)
    admins = models.ManyToManyField(User, related_name='competition_admins', blank=True, null=True)
    modified_by = models.ForeignKey(User, related_name='competitioninfo_modified_by',on_delete=models.CASCADE)
    last_modified = models.DateTimeField(auto_now_add=True)
    # pagecontainers = generic.GenericRelation(PageContainer)
    published = models.BooleanField(default=False, verbose_name="Publicly Available")
    datasets = models.ManyToManyField(Dataset, blank=True, related_name='phase')
    scoring_program = models.FileField(upload_to='scoring_program_file',null=True,blank=True, verbose_name="Scoring Program")
    conditional = models.TextField(null=True,blank=True)
    golden_file = models.FileField(upload_to='scoring_program_file',null=True,blank=True, verbose_name="golden")
    docker_config = models.FileField(upload_to='dockerfiles', default=None, blank=True)
    # default_docker_image = models.CharField(max_length=128, default='', blank=True)
    # disable_custom_docker_image = models.BooleanField(default=True)
    requirements = models.FileField(upload_to='requirement/%Y/%m/%d/',default=None,blank=True,null=True)
    ingestion_program = models.FileField(
        upload_to='ingestion_program',
        blank=True,
        null=True,
    )
    ingestion_program_docker_image = models.CharField(max_length=128, default='', blank=True)
    ingestion_program_organizer_dataset = models.ForeignKey(
        OrganizerDataSet,
        null=True,
        blank=True,
        related_name="ingestion_program_organizer_dataset",
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("comp_detail",kwargs={"pk":self.id})

    def get_count_participants(self):
        participants = CompetitionSubmission.objects.filter(competition=self).distinct('participant').count()
        return participants

    def get_top3(self):
        leader_board = CompetitionSubmission.objects.filter(competition=self,is_public=True).order_by('-score')[:3]
        return leader_board

    def get_submission_date(self):
        dates=[]
        dates_obj = CompetitionSubmission.objects.filter(competition=self).distinct('submitted_at__date')
        for date in dates_obj:
            dates.append(str(date.submitted_at.strftime("%Y-%m-%d")))
        return dates

    def get_total_submissiom(self):
        total=[]
        dates = CompetitionSubmission.objects.filter(competition=self).distinct('submitted_at__date')
        for date in dates:
            subm = CompetitionSubmission.objects.filter(competition=self, submitted_at__date=date.submitted_at).count()
            total.append(subm)
        return total

    def get_best_scores(self):
        scores=[]
        comp=self
        dates = CompetitionSubmission.objects.filter(competition=self).distinct('submitted_at__date')
        for date in dates:
            subm = CompetitionSubmission.objects.filter(competition=self, submitted_at__date=date.submitted_at).order_by('score').first()
            scores.append(subm.score)
        return scores


    def get_convas_data(self):
        # return date array
        #        high scores
        #        total submissions per day
        pass



class CompetitionSubmission(models.Model):
    """Represents a submission from a competition participant."""
    TYPES = (
        ("submitting", "submitting"),
        ("submitted", "submitted"),
        ("running", "running"),
        ("failed", "failed"),
        ("cancelled", "cancelled"),
        ("finished", "finished"),
        ("None", "None")
    )
    participant = models.ForeignKey(User, related_name='submissions',on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition, related_name='submissions',on_delete=models.CASCADE)
    secret = models.CharField(max_length=128, default='', blank=True)
    docker_image = models.CharField(max_length=128, default='', blank=True)
    file = models.FileField(upload_to='submission_file_name',  null=True, blank=True)
    description = models.CharField(max_length=256, blank=True)
    inputfile = models.FileField(upload_to='submission_inputfile',  null=True, blank=True)
    runfile = models.FileField(upload_to='submission_runfile',  null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    submission_number = models.PositiveIntegerField(default=0)
    output_file = models.FileField(upload_to='submission_output',  null=True, blank=True)
    exception_details = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=64, choices=TYPES, default="None")
    method_name = models.CharField(max_length=20, null=True, blank=True)
    method_description = models.TextField(null=True, blank=True)
    project_url = models.URLField(null=True, blank=True)
    publication_url = models.URLField(null=True, blank=True)
    team_name = models.CharField(max_length=64, null=True, blank=True)

    is_public = models.BooleanField(default=False)

    download_count = models.IntegerField(default=0)

    like_count = models.IntegerField(default=0)
    dislike_count = models.IntegerField(default=0)
    score = models.FloatField(default=0.0)
