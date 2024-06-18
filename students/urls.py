from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    path('mylearning/', views.StudentCourseListAPIView.as_view(), name='student_mylearning'),
    path('course/<slug:slug>/modules/', views.StudentCourseModulesListAPIView.as_view(), name='student_course_module_list'),
    path('module/<slug:slug>/contents/', views.StudentModuleContentListAPIView.as_view(), name='student_module_content_list'),
    path('courses/<slug:slug>/enroll/',
        views.CourseEnrollView.as_view(),
        name='course_enroll'),
]