import os
import subprocess
import requests
from celery import shared_task
from django.core.mail import send_mail
from .models import Course, Content, Video
from django.conf import settings
from moviepy.editor import VideoFileClip
from time import sleep
import logging

URL = settings.TRANSCRIPT_MODEL_URL
MEDIA_ROOT = settings.MEDIA_ROOT

logger = logging.getLogger(__name__)

def convert_video_to_audio(video_path, audio_path):
    """
    Run FFmpeg command to extract audio from the video
    """
    if os.path.exists(audio_path):
        print(f"Audio file already exists at {audio_path}")
        return

    try:
        video = VideoFileClip(video_path)
        video.audio.write_audiofile(audio_path)    
    except Exception as e:
        raise RuntimeError(f"Converting video to audio failed with error code {e.returncode}.")


# Celery Tasks
@shared_task
def transcript(id):
    """
    extract text from videos and save it in database
    """
    try:
        # Get the course by id
        course = Course.objects.get(id=id)

        # Iterate over modules related to the course
        for module in course.modules.all():

            # Iterate over contents related to the module
            for content in module.contents.all():
                item = content.item

                # Check if the item is Video
                if isinstance(item, Video):
                    # Check if video already transcripted 
                    if item.transcript:
                        return
                    
                    video_path = f"{MEDIA_ROOT}/{item.file}"
                    extracted_audio_path =  f"{MEDIA_ROOT}/audios/{item.id}.mp3"

                    convert_video_to_audio(video_path, extracted_audio_path)

                    with open(extracted_audio_path, "rb") as f:
                        data = f.read()
                    r = requests.post(URL, headers=headers, data=data)
                    print(r.json())

                    # save extracted text in database
                    item.transcript = r.json()['text']
                    item.save()
    except Course.DoesNotExist:
        print("Course not found")
    except Exception as e:
        print(f"An error occurred: {e}")

@shared_task
def transcript_video(id, *args, **kwargs):
    print(id)
    try:
        obj = Video.objects.get(id=id)

        if obj.transcript:
            return
        
        video_path = f"{MEDIA_ROOT}/{obj.file}"
        extracted_audio_path =  f"{MEDIA_ROOT}/audios/{obj.id}.mp3"
        convert_video_to_audio(video_path, extracted_audio_path)
        with open(extracted_audio_path, "rb") as f:
            data = f.read()
        for i in range(5):
            r = requests.post(URL, data=data)
            response = r.json()
            if 'error' not in response:
                obj.transcript = response['text']
                obj.save()
                break
            else:
                logger.error(f"Transcription error: {response['error']}")
            sleep(10)
    except Exception as e:
        logger.exception(f"Failed to transcribe video {id}: {e}")