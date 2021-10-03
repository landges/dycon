from django.urls import path
from .views import SubmitContest

urlpatterns = [
    path('', SubmitContest.as_view(),name='submit'),
]
