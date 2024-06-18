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
