from django.urls import path
from .views import *

urlpatterns = [
    path('change-status/',change_leaderboard,name="change"),
    path('competitions/', CompetionList.as_view(),name="competitions"),
    path('competitions/<int:pk>/', SubmitContest.as_view(),name='comp_detail'),
    path('competitions/<int:pk>/results/',get_result_csv,name="get_result"),
    path('uploadsubm/',UploadSubmission.as_view(),name='ajax_upload'),
    path('accounts/signup/',SignUp.as_view(),name='signup'),
    path('accounts/signout/',SignOut.as_view(),name='signout'),
]
