from django.forms import fields, widgets
from django import forms
from .models import *

class CompetitionSubmission(forms.ModelForm):
	class Meta:
		model=CompetitionSubmission
		filds = ('team_name','method_name','method_description','inputfile')