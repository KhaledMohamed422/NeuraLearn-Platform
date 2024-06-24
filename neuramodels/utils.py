import requests
from courses.models import Course, Module, Content, Video ,ContentType
from NeuraLearn.settings.base import SERVER_MODEL_URL

def get_course_transcripts(course_slug):

    course = Course.objects.get(slug=course_slug)    
    video_content_type = ContentType.objects.get(model='video')

    modules = course.modules.all()

    all_transcripts = ""

    for module in modules:
        print(module)
        video_contents = Content.objects.filter(module=module, content_type=video_content_type)
        
        for content in video_contents:
            video = Video.objects.get(id=content.object_id)
            if video.transcript:
                all_transcripts += video.transcript + "\n"
    print(f"**************************************All transcripts: {all_transcripts}**************************************")
    return all_transcripts


def generate_questions(text : str) -> str:
    pass


def generate_answer(course_slug,question,chat_history=[],k=3) -> dict:
    
    context = get_course_transcripts(course_slug)
    if not context:
        context = ""
    payload = {
    "context": context,
    "question": question,
    "k": k,
    "type": 3,
    "chat_history": chat_history,
    "do_spilting": True,
    "add_to_history": True,
    "chunk_size": 400,
    "chunk_overlap":50
    }
    response = requests.post(url=f"{SERVER_MODEL_URL}/neuarlearn/ml/chat", json=payload)
    return response
