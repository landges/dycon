from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.views.generic.base import View
from django.contrib.auth.models import User
from .tasks import *
from .models import *
from .forms import SignUpForm, CompetitionSubmissionForm, CompetitionForm
from django.http import JsonResponse
from io import StringIO
from django.http import JsonResponse, HttpResponse
import csv
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class SubmitContest(LoginRequiredMixin,View):
	login_url = '/accounts/login/'

	def get(self, request, pk):
		comp = Competition.objects.get(id=pk)
		# submission.delay(2,2)
		user = User.objects.get(username=request.user)
		
		leader_board = CompetitionSubmission.objects.filter(competition=comp,is_public=True).order_by('-score')		
		for result in leader_board:
			entries = CompetitionSubmission.objects.filter(competition=comp, participant=result.participant).count()
			result.entries = entries
		user_board = CompetitionSubmission.objects.filter(competition=comp, participant=user).order_by('submitted_at')
		details = comp.pages.filter(type="detail")
		participate= comp.pages.filter(type="participate")
		last_subm = user_board.first()
		return render(request,'contest/competition_detail.html',context={
			"competition":comp, 
			"leader_board":leader_board,
			"user_board":user_board,
			"details_pages":details,
			"participate_pages":participate,
			"last_subm":last_subm})

	def post(self, request):
		pass

class CompetionList(View):
	def get(self, request):
		comps = Competition.objects.filter(published=True)
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

class CreateCompetition(View):
	def get(self,request):
		form = CompetitionForm(request.POST)
		return render(request,'contest/create_comp.html',context={"form":form})

	def post(self,request):
		form = CompetitionForm(request.POST,request.FILES)
		if form.is_valid():
			comp = form.save()
			load_contest.delay(comp.id)
		return redirect("competitions")

# async def handle_uploaded_file(f):
# 	async with aiofiles.open(f"submission_inputfile/{f.name}", "wb+") as destination:
# 		for chunk in f.chunks():
# 			await destination.write(chunk)

# def _get_user(username):
# 	return User.objects.get(username=username)

# get_user = sync_to_async(_get_user,thread_sensitive=True)

# async def UploadSubmission(request):
# 	data=request.POST
# 	print(data)
# 	form = CompetitionSubmissionForm(request.POST,request.FILES)
# 	participant = get_user(request.username)
# 	form.instance.participant = participant
# 	if form.is_valid():
# 		await handle_uploaded_file(request.FILES["file"])
# 		subm = form.save()

# 		# submission(subm.id)
# 		submission_new.delay(subm.id)
# 		return render(request,'contest/includes/result_user_card.html',context={"result":subm})
# 		# return JsonResponse({"save":"OK"})
# 	else:
# 		return JsonResponse({"save":"Error"})

class UploadSubmission(View):
	def post(self,request):
		data=request.POST
		form = CompetitionSubmissionForm(request.POST,request.FILES)
		print(request.FILES)
		participant = User.objects.get(username=request.user)
		form.instance.participant = participant
		if form.is_valid():
			subm = form.save()
			subm.status = "submitting"
			subm.save()
			# submission(subm.id)
			submission_new.delay(subm.id)
			return render(request,'contest/includes/result_user_card.html',context={"result":subm})
			# return JsonResponse({"save":"OK"})
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