from django.contrib import admin
from .models import *
from django import forms
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget
# Register your models here.


class PageCompetitionInline(admin.TabularInline):
    model = PageCompetition
    extra = 1

class PageCompetitionAdminForm(forms.ModelForm):
    content = forms.CharField(label='Описание', widget=CKEditorUploadingWidget())

    class Meta:
        model = PageCompetition
        fields = '__all__'

@admin.register(Competition)
class CompetitionAdmin(admin.ModelAdmin):
	list_display=['id','title','published']
	list_editable = ("published",)
	inlines = [PageCompetitionInline]

@admin.register(CompetitionSubmission)
class CompetitionSubmissionAdmin(admin.ModelAdmin):
	list_display=['id','participant','score','is_public']

@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
	list_display = ['id','creator','name']

@admin.register(OrganizerDataSet)
class OrganizerDataSetAdmin(admin.ModelAdmin):
	list_display=['id','name','type']

@admin.register(PageCompetition)
class PageCompetitionAdmin(admin.ModelAdmin):
	list_display = ['id','title','competition']
	form= PageCompetitionAdminForm
	prepopulated_fields = {'slug': ('title',)}
