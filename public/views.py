from rest_framework import generics
from rest_framework.generics import get_object_or_404
from courses.models import Subject, Course
from drf_spectacular.utils import extend_schema
from .serializers import PublicCourseSerializer,  PublicCourseModuleSerializer

@extend_schema(tags=['Public Courses'])
class CourseListAPIView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = PublicCourseSerializer
    authentication_classes = []
    permission_classes = []

    def get_queryset(self):
        qs = super().get_queryset()
        slug = self.kwargs.get('subject')
        if slug:
            subject = get_object_or_404(Subject, slug=slug)
            qs = qs.filter(subject=subject)
        return qs.filter(available=True)

@extend_schema(tags=['Public Courses'])
class CourseDetailAPIView(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = PublicCourseModuleSerializer
    authentication_classes = []
    permission_classes = []
    lookup_field = 'slug'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(available=True)