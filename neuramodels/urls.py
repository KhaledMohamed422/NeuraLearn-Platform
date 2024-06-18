from django.urls import path
from . import views

app_name = 'neuramodels'

urlpatterns = [
    path('module/<slug:slug>/transcripts/', views.module_get_transcripts, name='module-get-transcripts'),
    path('video/<int:id>/transcript/', views.VideoGetTranscripts.as_view, name='video-get-transcript'),
    path('summarize/', views.Summarizer.as_view(), name='summarizer'),
]