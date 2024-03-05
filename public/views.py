from rest_framework import generics
from rest_framework.generics import get_object_or_404
from courses.models import Subject, Course
from .serializers import CourseSerializer, CourseModuleSerializer

class CourseListAPIView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        slug = self.kwargs.get('subject')
        if slug:
            subject = get_object_or_404(Subject, slug=slug)
            qs = qs.filter(subject=subject)
        return qs.filter(available=True)


class CourseDetailAPIView(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseModuleSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(available=True)