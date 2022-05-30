from django.urls import path
from .views import *

urlpatterns = [
    path('competitions/', CompetitionListView.as_view()),
]
