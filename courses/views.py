from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import get_object_or_404
from django.apps import apps
from .mixins import CourseOwnerMixin
from .models import Course, Module, Content
from .permissions import ( 
    IsModuleOwnerPermission,
    IsInstructorPermission,
)
from .serializers import (
    ManageCourseSerializer,
    CourseSerializer,
    CourseModuleSerializer,
    CourseDetailSerializer,
    ModuleSerializer,
    ModuleContentSerializer,
    TextSerializer,
    FileSerializer,
    ImageSerializer,
    VideoSerializer,
)


#------------------
# Courses API Views
#------------------
class CourseListAPIView(CourseOwnerMixin, generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = ManageCourseSerializer
    permission_classes = [IsInstructorPermission]

class CourseCreateAPIView(generics.CreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsInstructorPermission]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class CourseDetailAPIView(CourseOwnerMixin, generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseDetailSerializer
    permession_classes = [permissions.IsAdminUser, IsInstructorPermission]
    lookup_field = 'slug'
 
class CourseUpdateAPIView(CourseOwnerMixin, generics.RetrieveUpdateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permession_classes = [permissions.IsAdminUser, IsInstructorPermission]
    lookup_field = 'slug'

class CourseDeleteAPIView(CourseOwnerMixin, generics.RetrieveDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permession_classes = [permissions.IsAdminUser, IsInstructorPermission]
    lookup_field = 'slug'

class CourseModulesListAPIView(CourseOwnerMixin, generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseModuleSerializer
    permession_classes = [permissions.IsAdminUser, IsInstructorPermission]
    lookup_field = 'slug'


#------------------
# Modules API Views
#------------------
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

class ModuleRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    permission_classes = [IsInstructorPermission]

    def get_object(self):
        slug = self.kwargs.get('slug')
        return get_object_or_404(Module, slug=slug, course__owner=self.request.user)

class ModuleRetrieveDestroyAPIView(generics.RetrieveDestroyAPIView):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    permission_classes = [IsInstructorPermission]
    
    def get_object(self):
        slug = self.kwargs.get('slug')
        return get_object_or_404(Module, slug=slug, course__owner=self.request.user)

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
        return super().dispatch(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        module = self.module
        content = serializer.save(owner=self.request.user)
        Content.objects.create(module=module, item=content)

    def get_queryset(self):
        qs = self.model.objects.all()
        return qs
   
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