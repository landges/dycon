from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.views.generic.base import View
from django.contrib.auth.models import User
from .tasks import submission
from .models import *
from .forms import SignUpForm

# Create your views here.
class SubmitContest(View):
	def get(self, request, pk):
		comp = Competition.objects.get(id=pk)
		submission.delay(2,2)
		user = User.objects.get(username=request.user)
		leader_board = CompetitionSubmission.objects.filter(competition=comp,is_public=True).order_by('score')		
		user_board = CompetitionSubmission.objects.filter(competition=comp, participant=user).order_by('submitted_at')
		return render(request,'contest/competition_detail.html',context={
			"competition":comp, 
			"leader_board":leader_board,
			"user_board":user_board})

	def post(self, request):
		pass

class CompetionList(View):
	def get(self, request):
		comps = Competition.objects.all()
		return render(request,'contest/competitions_list.html',context={"competitions":comps})

	def post(self, request):
		pass

class SignUp(View):
	def get(self, request):
		form = SignUpForm()
		return render(request, 'registration/registration.html', context={"form":form})

	def post(self,request):
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect("competitions")

class SignOut(View):
	def get(self,request):
		logout(request)
		return redirect("competitions")