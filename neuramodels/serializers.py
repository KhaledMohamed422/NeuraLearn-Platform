from rest_framework import serializers
from courses.models import Video, Text

class VideoTranscriptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['title', 'transcript']

class Transcripts(serializers.Serializer):
    text = serializers.CharField(style={'base_template': 'textarea.html'})

class SummarizerSerializer(serializers.Serializer):
    summary = serializers.CharField()

class QuestionGenerationSerializer(serializers.Serializer):
    transcript = serializers.CharField(max_length=5000)

class ChatBotRequestSerializer(serializers.Serializer):
    context = serializers.CharField(max_length=5000)
    question = serializers.CharField(max_length=1000)
    chat_history = serializers.JSONField()
    k = serializers.IntegerField()

class ChatBotResponseSerializer(serializers.Serializer):
    response = serializers.CharField(max_length=5000)
