from django.urls import path
from . import views

app_name = 'public'

urlpatterns = [
    path('courses/', views.CourseListAPIView.as_view(), name='course_list'),
    path('subject/<slug:subject>/',
        views.CourseListAPIView.as_view(),
        name='course_list_subject'),
    path('course/<slug:slug>/detail/', 
        views.CourseDetailAPIView.as_view(),
        name='course_detail')
]