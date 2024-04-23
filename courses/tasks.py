import os
import subprocess
import requests
from celery import shared_task
from django.core.mail import send_mail
from .models import Course, Content, Video
from django.conf import settings

URL = settings.TRANSCRIPT_MODEL_URL
TOKEN = settings.TRANSCRIPT_TOKEN
MEDIA_ROOT = settings.MEDIA_ROOT

headers = {"Authorization": f"Bearer {TOKEN}"}

def convert_video_to_audio(video_path, audio_path):
    """
    Run FFmpeg command to extract audio from the video
    """
    if os.path.exists(audio_path):
        print(f"Audio file already exists at {audio_path}")
        return
    
    try:
        subprocess.run(['ffmpeg', '-i', video_path, '-vn', '-acodec', 'libmp3lame', audio_path], check=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"FFmpeg command failed with error code {e.returncode}.") from e

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
