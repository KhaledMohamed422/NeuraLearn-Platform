import requests
from courses.models import Course, Module, Content, Video ,ContentType
from NeuraLearn.settings.base import SERVER_MODEL_URL

def get_course_transcripts(course_slug):

    course = Course.objects.get(slug=course_slug)    
    video_content_type = ContentType.objects.get(model='video')

    modules = course.modules.all()

    all_transcripts = ""

    for module in modules:

        video_contents = Content.objects.filter(module=module, content_type=video_content_type)
        
        for content in video_contents:
            video = Video.objects.get(id=content.object_id)
            if video.transcript:
                all_transcripts += video.transcript + "\n"

    return all_transcripts

def get_module_transcripts(module_slug):

    module = Module.objects.get(slug=module_slug)
    video_content_type = ContentType.objects.get(model='video')

    all_transcripts = ""


    video_contents = Content.objects.filter(module=module, content_type=video_content_type)
    
    for content in video_contents:
        video = Video.objects.get(id=content.object_id)
        if video.transcript:
            all_transcripts += video.transcript + "\n"

    return all_transcripts

def generate_questions(text : str) -> str:
    final_questions = []

    list_of_text = [one_video_transcript for one_video_transcript in text.split('$#@') if one_video_transcript]
    print(list_of_text)
    
    return {"key" , True}
    # for text in list_of_text:
    #     print(type(text))
    #     payload = {"transcript":text,"types":[0 , 1],"chunk_size":3000,'chunk_overlap':500}
    #     response = requests.post(url=f"{SERVER_MODEL_URL}/neuarlearn/ml/QuestionGeneration", json=payload)
    #     final_questions.append(response.json())
    # # print(response.json())
    # return final_questions



def generate_answer(course_slug,question,chat_history=[],k=3) -> dict:
    
    context = get_course_transcripts(course_slug)
    if not context:
        context = "None Context"
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
