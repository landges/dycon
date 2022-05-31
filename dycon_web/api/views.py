from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from contest.tasks import submission_new
from rest_framework import generics, permissions
# Create your views here.

class CompetitionListView(APIView):
	permission_classes = [permissions.IsAuthenticated]

	def get(self, request):
		comps = Competition.objects.filter(published=True)
		serializer = CompetitionsListSerializer(comps, many=True)
		return Response(serializer.data)


class CompetitionDetailView(APIView):
	permission_classes = [permissions.IsAuthenticated]

	def get(self, request, pk):
		comp = Competition.objects.get(id=pk)
		serializer = CompetitionsDetailSerializer(comp)
		return Response(serializer.data)


# class CompetitionSubmissionCreateView(APIView):
# 	def post(self, request):
# 		comp_subm = CompetitionSubmissionCreateSerializer(data=request.data)
# 		if comp_subm.is_valid():
# 			comp_subm.save()
# 			submission_new.delay(comp_subm.id)
# 		return Response(status=201)

class CompetitionSubmissionCreateView(generics.CreateAPIView):
	serializer_class = CompetitionSubmissionCreateSerializer
	permission_classes = [permissions.IsAuthenticated]

	def perform_create(self, serializer):
		comp = serializer.save()
		submission_new.delay(comp.id)