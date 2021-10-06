from django.urls import path
from .views import *

urlpatterns = [
    path('competitions/', CompetionList.as_view(),name="competitions"),
    path('competitions/<int:pk>', SubmitContest.as_view(),name='comp_detail'),
]
