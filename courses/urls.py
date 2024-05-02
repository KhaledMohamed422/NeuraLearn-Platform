from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('subjects/',
         views.SubjectListView.as_view(),
         name='subject_list'),
    path('mine/', 
        views.CourseListAPIView.as_view(),
        name='manage_course_list'),
    path('create/',
        views.CourseCreateAPIView.as_view(),
        name='course_create'),
    path('<slug:slug>/detail/', 
        views.CourseDetailAPIView.as_view(),
        name="manage_course_detail"),
    path('<slug:slug>/edit/',
        views.CourseUpdateAPIView.as_view(),
        name='course_edit'),
    path('<slug:slug>/delete/',
        views.CourseDeleteAPIView.as_view(),
        name='course_delete'),
    path('<slug:slug>/publish/',
        views.CoursePublishView.as_view(),
        name='course_publish'),
    path('<slug:slug>/unpublish/',
        views.CourseUnPublishView.as_view(),
        name='course_unpublish'),
    path('<slug:slug>/modules/',
        views.CourseModulesListAPIView.as_view(),
        name="manage_course_modules_list"),
    path('<slug:slug>/module/create/',
        views.ModuleCreateAPIView.as_view(),
        name="module_create"),
    path('module/<slug:slug>/update/',
        views.ModuleUpdateAPIView.as_view(),
        name='module_update'),
    path('module/<slug:slug>/delete/',
        views.ModuleDestroyAPIView.as_view(),
        name='module_delete'),
    path('module/<slug:slug>/contents/',
        views.ModuleContentListAPIView.as_view(),
        name='manage_module_content_list'),
    path('module/<slug:slug>/content/<str:model_name>/create/',
        views.ContentCreateAPIView.as_view(),
        name='module_content_create'),
    path('module/content/<str:model_name>/<uuid:uuid>/',
        views.ContentRetrieveUpdateDestroyAPIView.as_view(),
        name='content_update'),
]