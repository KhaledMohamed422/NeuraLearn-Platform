import requests
from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from courses.models import Module, Video
from time import sleep
from .serializers import (VideoTranscriptSerializer,
                          SummarizerSerializer,
                          Transcripts ,
                          QuestionGenerationSerializer,
                          ChatBotRequestSerializer,
                          ChatBotResponseSerializer)
from .utils import generate_questions , generate_answer

URL = settings.SUMMARIZER_MODEL_URL
TOKEN = settings.SUMMARIZER_TOKEN

"""
    Summarization
        - endpoint for get all transiscripts of specified section
            * Input: section-slug
            * Output: all transcripts
        - endpoint for generate summarization
            * Input: text
            * output: summrize
""" 
@extend_schema(
    tags=['Summarizer'],
    description="Retrieve the transcript for all videos in a module.",
    responses={
        200: OpenApiResponse(response=VideoTranscriptSerializer(many=True), description='List of video transcripts'),
        400: OpenApiResponse(description='Transcript not generated yet'),
        404: OpenApiResponse(description='Module not found')
    }
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def module_get_transcripts(request, slug=None):
    module = get_object_or_404(Module, slug=slug, course__owner=request.user)
    data = []

    for content in module.contents.all():
        item = content.item

        # Check if the item is Video
        if isinstance(item, Video):
            # Check if video already transcripted 
            if item.transcript:
                data.append(VideoTranscriptSerializer(item).data)
            else:
                return Response(
                    {"error": f"Transcript for video '{item.title}' is not generated yet, please wait some time."},
                    status=status.HTTP_400_BAD_REQUEST
                )
    
    return Response(data, status=status.HTTP_200_OK)

@extend_schema(
    tags=['Summarizer'],
    request=Transcripts,
    responses={
        200: OpenApiResponse(response=SummarizerSerializer),
        400: OpenApiResponse(description='Transcript not generated yet'),
        404: OpenApiResponse(description='Module not found')
    }
)
class Summarizer(APIView):
    permission_classes = []
    serializer_class = Transcripts


    # def get_serializer(self, *args, **kwargs):
    #     return Transcripts(*args, **kwargs)
    def post(self, request):
        serializer = Transcripts(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data['text']
            # try 5 times if one request is valid then return response
            for i in range(5):
                response = requests.post(url="http://127.0.0.1:8080/neuarlearn/ml/summaizer", json={"text":data, "min_length": 50, "max_length": 250})
                print(type(response.json()))
                data = response.json()[0]
                if response.status_code == 200 and not data.get('error'):
                    output_serializer = SummarizerSerializer(data={"summary": data.get('generated_text')})
                    if output_serializer.is_valid():
                        return Response(output_serializer.data)
                    return Response(output_serializer.errors, status=400)
                sleep(20)
            return Response(response.json(), status=response.status_code)
        return Response(serializer.errors, status=400)
    

@extend_schema(
    tags=['Question Generation'],
    responses={200: VideoTranscriptSerializer(many=True)},
    request = VideoTranscriptSerializer
    # parameters=[
    #     {
    #         'name': 'id',
    #         'required': True,
    #         'location': 'path',
    #         'description': 'ID of the video to retrieve transcript for',
    #         'schema': {'type': 'integer'}
    #     }
    # ]
)
class VideoGetTranscript(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id=None):
        video = get_object_or_404(Video, id=id, owner=request.user)
        data = {}

        # Check if video already transcripted 
        if video.transcript:
            data = VideoTranscriptSerializer(video).data
        else:
            return Response(
                {"error": f"Transcript for video '{video.title}' is not generated yet, please wait some time."},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(data, status=status.HTTP_200_OK)

@extend_schema(
    tags=['Question Generation'],
    request=QuestionGenerationSerializer,
    responses={200: dict}
)
class QuestionGeneration(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = QuestionGenerationSerializer(data=request.data)
        if serializer.is_valid():
            transcript = serializer.validated_data['transcript']
            questions = generate_questions(transcript)
            return Response({"questions": questions}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    tags=['Question Answer (chatbot)'],
    request=ChatBotRequestSerializer,
    responses={200: ChatBotResponseSerializer(many=True)}
)
class ChatBotAPIView(APIView):
    def post(self, request):
        serializer = ChatBotRequestSerializer(data=request.data)
        if serializer.is_valid():
            context = serializer.validated_data['context']
            question = serializer.validated_data['question']
            chat_history = serializer.validated_data['chat_history']
            k = serializer.validated_data['k']
            
            # Send data to the model server
            payload = {
                "context": context,
                "question": question,
                "chat_history": chat_history ,
                "k" : k
            }
            response = generate_answer(payload)
            if response.status_code == 200:
                response_data = response.json()
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Model server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

