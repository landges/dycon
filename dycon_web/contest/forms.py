from django.forms import fields, widgets
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

class CompetitionSubmissionForm(forms.ModelForm):
	class Meta:
		model=CompetitionSubmission
		fields = ('competition','team_name','method_name','method_description','inputfile')


class SignUpForm(UserCreationForm):
	class Meta:
		model = User
		fields = ('username','email','password1','password2')