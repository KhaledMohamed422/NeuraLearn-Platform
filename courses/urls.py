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
    # path('<slug:slug>/publish/',
    #     views.CoursePublishView.as_view(),
    #     name='course_publish'),
    # path('<slug:slug>/unpublish/',
    #     views.CourseUnPublishView.as_view(),
    #     name='course_unpublish'),
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
    path('module/<slug:slug>/content/text/create/',
        views.ContentTextCreateAPIView.as_view(),
        name='module_content_text_create'),
    path('module/<slug:slug>/content/file/create/',
        views.ContentFileCreateAPIView.as_view(),
        name='module_content_file_create'),
    path('module/<slug:slug>/content/image/create/',
        views.ContentImageCreateAPIView.as_view(),
        name='module_content_image_create'),
    path('module/<slug:slug>/content/video/create/',
        views.ContentVideoCreateAPIView.as_view(),
        name='module_content_video_create'),
    path('module/content/text/<int:id>/',
        views.ContentTextUpdateDestroAPIView.as_view(),
        name='content_text_update_delete'),
    path('module/content/file/<int:id>/',
        views.ContentFileUpdateDestroAPIView.as_view(),
        name='content_file_update_delete'),
    path('module/content/image/<int:id>/',
        views.ContentImageUpdateDestroAPIView.as_view(),
        name='content_image_update_delete'),
    path('module/content/video/<int:id>/',
        views.ContentVideoUpdateDestroAPIView.as_view(),
        name='content_video_update_delete'),
]