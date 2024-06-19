from django.urls import path
from . import views

app_name = 'neuramodels'

urlpatterns = [
    path('module/<slug:slug>/transcripts/', views.module_get_transcripts, name='module-get-transcripts'),
    path('video/<int:id>/transcript/', views.VideoGetTranscript.as_view(), name='video-get-transcript'),
    path('summarize/', views.Summarizer.as_view(), name='summarizer'),
    path('generate-questions/', views.QuestionGeneration.as_view(), name='question_generation'),
]