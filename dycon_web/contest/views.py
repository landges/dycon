from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.views.generic.base import View
from django.contrib.auth.models import User
from .tasks import *
from .models import *
from .forms import SignUpForm, CompetitionSubmissionForm
from django.http import JsonResponse
from io import StringIO
from django.http import JsonResponse, HttpResponse
import csv

# Create your views here.
class SubmitContest(View):
	def get(self, request, pk):
		comp = Competition.objects.get(id=pk)
		# submission.delay(2,2)
		user = User.objects.get(username=request.user)
		leader_board = CompetitionSubmission.objects.filter(competition=comp,is_public=True).order_by('score')		
		for result in leader_board:
			entries = CompetitionSubmission.objects.filter(competition=comp, participant=result.participant).count()
			result.entries = entries
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

def change_leaderboard(request):
	data=request.POST
	subm = CompetitionSubmission.objects.get(id=data.get('id'))
	user = User.objects.get(username=request.user)
	publ_subm = CompetitionSubmission.objects.filter(competition=subm.competition, participant=user,is_public=True).first()
	if publ_subm is not None:
		publ_subm.is_public = False
		publ_subm.save()
	subm.is_public= not subm.is_public
	subm.save()
	publ_subm = CompetitionSubmission.objects.filter(competition=subm.competition, participant=user,is_public=True).first()
	if publ_subm is None:
		return JsonResponse({"status":"NO"})
	else:
		return JsonResponse({"status":"OK"})

def get_result_csv(request,pk):
	comp=Competition.objects.get(id=pk)
	leader_board = CompetitionSubmission.objects.filter(competition=comp,is_public=True).order_by('score')		
	for result in leader_board:
		entries = CompetitionSubmission.objects.filter(competition=comp, participant=result.participant).count()
		result.entries = entries
	# leader_board.values('id','participant','score')
	csvfile = StringIO()
	csvwriter = csv.writer(csvfile)
	for result in leader_board:
		csvwriter.writerow((result.id,result.participant,result.score))
	response = HttpResponse(csvfile.getvalue(),status=200, content_type="css/text")
	response["Content-Disposition"] = "attachment;filename=result.csv"
	return response



class UploadSubmission(View):
	def post(self,request):
		data=request.POST
		print(data)
		form = CompetitionSubmissionForm(request.POST,request.FILES)
		participant = User.objects.get(username=request.user)
		form.instance.participant = participant
		if form.is_valid():
			subm = form.save()
			# submission(subm.id)
			submission_new.delay(subm.id)
			return JsonResponse({"save":"OK"})
		else:
			return JsonResponse({"save":"Error"})


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