from django.shortcuts import render, redirect
from django.views.generic.base import View
from .tasks import submission

# Create your views here.
class SubmitContest(View):
	def get(self, request):
		print('hello')
		submission.delay(2,2)		
		return render(request,'contest/competition_detail.html',context={})

	def post(self, request):
		pass