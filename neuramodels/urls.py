from django.urls import path
from . import views

app_name = 'neuramodels'

urlpatterns = [
    # path('module/<slug:slug>/transcripts/', views.module_get_transcripts, name='module-get-transcripts'),
    path('module/<slug:slug>/transcripts/', views.GetTranscript.as_view(), name='module-get-transcripts'),
    path('summarize/', views.Summarizer.as_view(), name='summarizer'),
    path('generate-questions/', views.QuestionGenerationView.as_view(), name='question_generation'),
    path('chatbot/', views.ChatBotAPIView.as_view(), name='chatbot'),
]