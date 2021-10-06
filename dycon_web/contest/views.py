from django.shortcuts import render, redirect
from django.views.generic.base import View
from .tasks import submission
from .models import *

# Create your views here.
class SubmitContest(View):
	def get(self, request, pk):
		comp = Competition.objects.get(id=pk)
		submission.delay(2,2)		
		return render(request,'contest/competition_detail.html',context={"competition":comp})

	def post(self, request):
		pass

class CompetionList(View):
	def get(self, request):
		comps = Competition.objects.all()
		return render(request,'contest/competitions_list.html',context={"competitions":comps})

	def post(self, request):
		pass