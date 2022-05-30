from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
# Create your views here.

class CompetitionListView(APIView):
	def get(self, request):
		comps = Competition.objects.filter(published=True)
		serializer = CompetitionsListSerializer(comps, many=True)
		return Response(serializer.data)