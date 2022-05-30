from rest_framework import serializers

from contest.models import *


class CompetitionsListSerializer(serializers.ModelSerializer):
	"""Вывод списка всех соревнований контеста"""

	class Meta:
		model = Competition
		fields = ('id','title','description')