from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Competition)
class CompetitionAdmin(admin.ModelAdmin):
	list_display=['id','title','published']

@admin.register(CompetitionSubmission)
class CompetitionSubmissionAdmin(admin.ModelAdmin):
	list_display=['id','participant']

@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
	list_display = ['id','creator','name']

@admin.register(OrganizerDataSet)
class OrganizerDataSetAdmin(admin.ModelAdmin):
	list_display=['id','name','type']

