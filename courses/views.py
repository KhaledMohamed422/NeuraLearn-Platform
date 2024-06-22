from rest_framework import generics, permissions, views, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from django.http import Http404
from drf_spectacular.utils import extend_schema
from django.apps import apps
from .tasks import transcript_video
from .mixins import CourseOwnerMixin
from .models import Course, Module, Content, Subject, Text, File, Image, Video
from .permissions import ( 
    IsModuleOwnerPermission,
    IsInstructorPermission,
)
from .serializers import (
    ManageCourseSerializer,
    CourseSerializer,
    CourseModuleSerializer,
    CourseDetailSerializer,
    CourseAvailableSerializer,
    ModuleSerializer,
    ModuleContentSerializer,
    TextSerializer,
    FileSerializer,
    ImageSerializer,
    VideoSerializer,
    SubjectSerializer,
)

@extend_schema(tags=['Subjects'])
class SubjectListView(generics.ListAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    pagination_class = None

#------------------
# Courses API Views
#------------------
@extend_schema(tags=['Courses'])
class CourseListAPIView(CourseOwnerMixin, generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = ManageCourseSerializer
    permission_classes = [IsInstructorPermission]

@extend_schema(tags=['Courses'])
class CourseCreateAPIView(generics.CreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsInstructorPermission]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

@extend_schema(tags=['Courses'])
class CoursePublishView(generics.GenericAPIView):
    permission_classes = [IsInstructorPermission]

    def put(self, request, slug, format=None):
        user = self.request.user
        course = get_object_or_404(Course, slug=slug, owner=user)
        if course.available:
            return Response({"Error": "Course is already published"}, 
                            status=status.HTTP_400_BAD_REQUEST)
        course.available = True
        course.save()
        serializer = CourseAvailableSerializer(course)
        return Response(serializer.data)

@extend_schema(tags=['Courses'])   
class CourseUnPublishView(generics.GenericAPIView):
    permission_classes = [IsInstructorPermission]

    def put(self, request, slug, format=None):
        user = self.request.user
        course = get_object_or_404(Course, slug=slug, owner=user)
        if not course.available:
            return Response({"Error": "Course is already unpublished"},
                            status=status.HTTP_400_BAD_REQUEST)
        
        course.available = False
        course.save()
        serializer = CourseAvailableSerializer(course)
        return Response(serializer.data)

@extend_schema(tags=['Courses'])
class CourseDetailAPIView(CourseOwnerMixin, generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseDetailSerializer
    permession_classes = [permissions.IsAdminUser, IsInstructorPermission]
    lookup_field = 'slug'
 
@extend_schema(tags=['Courses'])
class CourseUpdateAPIView(CourseOwnerMixin, generics.UpdateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permession_classes = [permissions.IsAdminUser, IsInstructorPermission]
    lookup_field = 'slug'

@extend_schema(tags=['Courses'])
class CourseDeleteAPIView(CourseOwnerMixin, generics.DestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permession_classes = [permissions.IsAdminUser, IsInstructorPermission]
    lookup_field = 'slug'

@extend_schema(tags=['Modules'])
class CourseModulesListAPIView(CourseOwnerMixin, generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseModuleSerializer
    permession_classes = [permissions.IsAdminUser, IsInstructorPermission]
    lookup_field = 'slug'


#------------------
# Modules API Views
#------------------
@extend_schema(tags=['Modules'])
class ModuleCreateAPIView(generics.CreateAPIView):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    permission_classes = [IsInstructorPermission]
    
    def perform_create(self, serializer):
        slug = self.kwargs.get('slug')
        course = get_object_or_404(Course, slug=slug)
        if course.owner != self.request.user:
            raise PermissionDenied("You don't have permission")
        serializer.save(course=course)

@extend_schema(tags=['Modules'])
class ModuleUpdateAPIView(generics.UpdateAPIView):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    permission_classes = [IsInstructorPermission]

    def get_object(self):
        slug = self.kwargs.get('slug')
        return get_object_or_404(Module, slug=slug, course__owner=self.request.user)

@extend_schema(tags=['Modules'])
class ModuleDestroyAPIView(generics.DestroyAPIView):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    permission_classes = [IsInstructorPermission]
    
    def get_object(self):
        slug = self.kwargs.get('slug')
        return get_object_or_404(Module, slug=slug, course__owner=self.request.user)

@extend_schema(tags=['Contents'])
class ModuleContentListAPIView(generics.RetrieveAPIView):
    queryset = Module.objects.all()
    serializer_class = ModuleContentSerializer
    permission_classes = [IsInstructorPermission]

    def get_object(self):
        slug = self.kwargs.get('slug')
        return get_object_or_404(Module, slug=slug, course__owner=self.request.user)


#------------------
# Content API Views
#------------------
@extend_schema(tags=['Contents'])
class ContentTextCreateAPIView(generics.CreateAPIView):
    queryset = Module.objects.all()
    serializer_class = TextSerializer
    permission_classes = [IsInstructorPermission]

    def perform_create(self, serializer):
        slug = self.kwargs.get('slug')
        module = get_object_or_404(Module,
                                       slug=slug,
                                       course__owner=self.request.user)
        content = serializer.save(owner=self.request.user)
        Content.objects.create(module=module, item=content)

@extend_schema(tags=['Contents'])
class ContentTextUpdateDestroAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Text.objects.all()
    serializer_class = TextSerializer
    permission_classes = [IsInstructorPermission]

    def get_object(self):
        id = self.kwargs.get('id')
        return generics.get_object_or_404(Text, id=id, owner=self.request.user)


@extend_schema(tags=['Contents'])
class ContentFileCreateAPIView(generics.CreateAPIView):
    queryset = Module.objects.all()
    serializer_class = FileSerializer
    permission_classes = [IsInstructorPermission]

    def perform_create(self, serializer):
        slug = self.kwargs.get('slug')
        module = get_object_or_404(Module,
                                       slug=slug,
                                       course__owner=self.request.user)
        content = serializer.save(owner=self.request.user)
        Content.objects.create(module=module, item=content)

@extend_schema(tags=['Contents'])
class ContentFileUpdateDestroAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    permission_classes = [IsInstructorPermission]

    def get_object(self):
        id = self.kwargs.get('id')
        return generics.get_object_or_404(File, id=id, owner=self.request.user)
    
@extend_schema(tags=['Contents'])
class ContentImageCreateAPIView(generics.CreateAPIView):
    queryset = Module.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [IsInstructorPermission]

    def perform_create(self, serializer):
        slug = self.kwargs.get('slug')
        module = get_object_or_404(Module,
                                       slug=slug,
                                       course__owner=self.request.user)
        content = serializer.save(owner=self.request.user)
        Content.objects.create(module=module, item=content)

@extend_schema(tags=['Contents'])
class ContentImageUpdateDestroAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [IsInstructorPermission]

    def get_object(self):
        id = self.kwargs.get('id')
        return generics.get_object_or_404(Image, id=id, owner=self.request.user)
    
@extend_schema(tags=['Contents'])
class ContentVideoCreateAPIView(generics.CreateAPIView):
    queryset = Module.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [IsInstructorPermission]

    def perform_create(self, serializer):
        slug = self.kwargs.get('slug')
        module = get_object_or_404(Module,
                                       slug=slug,
                                       course__owner=self.request.user)
        content = serializer.save(owner=self.request.user)
        print(content.id)
        transcript_video.delay(content.id)
        Content.objects.create(module=module, item=content)

@extend_schema(tags=['Contents'])
class ContentVideoUpdateDestroAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [IsInstructorPermission]

    def get_object(self):
        id = self.kwargs.get('id')
        return generics.get_object_or_404(Video, id=id, owner=self.request.user)