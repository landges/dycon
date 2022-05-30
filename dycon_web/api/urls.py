from django.urls import path
from .views import *

urlpatterns = [
    path('competitions/', CompetitionListView.as_view()),
    path('competitions/<int:pk>/',CompetitionDetailView.as_view()),
    path('uploadsubmission/',CompetitionSubmissionCreateView.as_view()),
]
