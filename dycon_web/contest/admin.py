from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Competition)
class CompetitionAdmin(admin.ModelAdmin):
	list_display=['id','title']