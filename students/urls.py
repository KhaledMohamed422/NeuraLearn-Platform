from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    path('courses/<slug>/enroll/',
        views.CourseEnrollView.as_view(),
        name='course_enroll'),
    path('course/<slug>/<slug:module_slug>/',
        views.StudentCourseDetailView.as_view(),
        name='student_course_detail_module'),
]