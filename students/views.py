from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication
from public.serializers import CourseSerializer
from .serializers import CourseModuleSerializer, ModuleSerializer
from courses.models import Course
from .permissions import IsAdminOrEnrolled
    
class StudentCourseListAPIView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsAdminOrEnrolled]
    
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(students__in=[self.request.user])

class StudentCourseDetailView(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseModuleSerializer
    permission_classes = [IsAuthenticated, IsAdminOrEnrolled] # TODO Create custom perm IsStudent.
    lookup_field = 'slug'

    def retrieve(self, *args, **kwargs):
        course = self.get_object()
        serializer = self.get_serializer(course)
        module_slug = self.kwargs.get('module_slug')
        if module_slug:
            module = course.modules.get(slug=module_slug)
            if module:
                data = serializer.data
                data['module'] = ModuleSerializer(module, context={'request': self.request}).data
            else:
                data['module'] = {"message": "there is no modulest yet"}
        return Response(data, status=status.HTTP_200_OK)

class CourseEnrollView(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request, slug, format=None):
        course = get_object_or_404(Course, slug=slug)
        course.students.add(request.user)
        return Response({"enrolled": True})