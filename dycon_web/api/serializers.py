from rest_framework import serializers

from contest.models import *


class CompetitionsListSerializer(serializers.ModelSerializer):
	"""Вывод списка всех соревнований контеста"""

	class Meta:
		model = Competition
		fields = ('id','title','description')




class CompetitionSubmissionCreateSerializer(serializers.ModelSerializer):

	class Meta:
		model = CompetitionSubmission
		fields = ("method_name",
			"method_description",
			"team_name",
			"inputfile",
			"competition",
			"participant"
			)



class CompetitionSubmissionsDetailSerializer(serializers.ModelSerializer):

	participant = serializers.SlugRelatedField(slug_field="username", read_only=True)

	class Meta:
		model = CompetitionSubmission
		fields = ("id",
			"description", 
			"submitted_at", 
			"status", 
			"method_name",
			"method_description",
			"team_name",
            "is_public",
            "score",
            "participant",)


class CompetitionsDetailSerializer(serializers.ModelSerializer):
	"""Вывод полной информации о соревновании"""


	creator = serializers.SlugRelatedField(slug_field="username", read_only=True)
	datasets = serializers.SlugRelatedField(slug_field="name",read_only=True, many=True)
	modified_by = serializers.SlugRelatedField(slug_field="username",read_only=True)
	admins = serializers.SlugRelatedField(slug_field="username",read_only=True,many=True)
	submissions = CompetitionSubmissionsDetailSerializer(many=True)

	class Meta:
		model = Competition
		exclude = ('requirements','ingestion_program','ingestion_program_docker_image','golden_file')