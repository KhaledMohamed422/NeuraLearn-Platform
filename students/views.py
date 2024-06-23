from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_spectacular.utils import extend_schema
from courses.models import Course, Module
from drf_spectacular.utils import extend_schema
from .serializers import StudentCourseSerializer, StudentCourseModulesSerializer, StudentModuleSerializer
from .permissions import IsAdminOrEnrolled, IsAdminOrEnrolledModule
    
@extend_schema(tags=['Students'])
class StudentCourseListAPIView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = StudentCourseSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(students__in=[self.request.user])

@extend_schema(tags=['Students'])
class StudentCourseModulesListAPIView(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = StudentCourseModulesSerializer
    permession_classes = [IsAuthenticated, IsAdminOrEnrolled]
    lookup_field = 'slug'

@extend_schema(tags=['Students'])
class StudentModuleContentListAPIView(generics.RetrieveAPIView):
    queryset = Module.objects.all()
    serializer_class = StudentModuleSerializer
    permession_classes = [IsAuthenticated, IsAdminOrEnrolledModule]
    lookup_field = 'slug'

@extend_schema(tags=['Students'])
class CourseEnrollView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [BasicAuthentication, JWTAuthentication]
    serializer_class = None

    def post(self, request, slug, format=None):
        course = get_object_or_404(Course, slug=slug)
        course.students.add(request.user)
        return Response({"enrolled": True})