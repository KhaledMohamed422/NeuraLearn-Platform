from rest_framework import generics, permissions, views, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from django.http import Http404
from drf_spectacular.utils import extend_schema
from django.apps import apps
from .mixins import CourseOwnerMixin
from .models import Course, Module, Content, Subject
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
class ContentCreateAPIView(generics.CreateAPIView):
    module = None 
    model = None
    queryset = None
    permission_classes = [IsInstructorPermission]

    def get_model(self, model_name):
        if model_name in ['text', 'video', 'image', 'file']:
            return apps.get_model(app_label='courses',
                                  model_name=model_name)
        return None

    def get_serializer_class(self):
        model = self.model.__name__
        if model == 'Text':
            return TextSerializer
        elif model == 'Video':
            return VideoSerializer
        elif model == 'Image':
            return ImageSerializer
        elif model == 'File':
            return FileSerializer
        return None

    def dispatch(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        model_name = kwargs.get('model_name')
        self.module = get_object_or_404(Module,
                                       slug=slug,
                                       course__owner=self.request.user)
        self.model = self.get_model(model_name)
        if self.model is None:
            raise Http404("Model not found")
        return super().dispatch(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        module = self.module
        content = serializer.save(owner=self.request.user)
        Content.objects.create(module=module, item=content)

    def get_queryset(self):
        qs = self.model.objects.all()
        return qs

@extend_schema(tags=['Contents'])
class ContentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    model = None
    obj = None 
    permission_classes = [IsInstructorPermission]

    def get_model(self, model_name):
        if model_name in ['text', 'video', 'image', 'file']:
            return apps.get_model(app_label='courses',
                                  model_name=model_name)
        return None

    def get_serializer_class(self):
        model = self.model.__name__
        if model == 'Text':
            return TextSerializer
        elif model == 'Video':
            return VideoSerializer
        elif model == 'Image':
            return ImageSerializer
        elif model == 'File':
            return FileSerializer
        return None

    def dispatch(self, request, *args, **kwargs):
        model_name = kwargs.get('model_name')
        uuid = kwargs.get('uuid')
        self.model = self.get_model(model_name)
        self.obj = get_object_or_404(Content,
                                         uuid=uuid,
                                         module__course__owner=request.user)
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        return None
    
    def get_object(self):
        return self.obj.item

    def perform_destroy(self, instance):
        self.obj.item.delete()
        self.obj.delete()