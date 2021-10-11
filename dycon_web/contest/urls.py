from django.urls import path
from .views import *

urlpatterns = [
    path('competitions/', CompetionList.as_view(),name="competitions"),
    path('competitions/<int:pk>', SubmitContest.as_view(),name='comp_detail'),
    path('uploadsubm/',UploadSubmission.as_view(),name='ajax_upload'),
    path('accounts/signup/',SignUp.as_view(),name='signup'),
    path('accounts/signout/',SignOut.as_view(),name='signout'),
]
