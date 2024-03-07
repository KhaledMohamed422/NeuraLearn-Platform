from rest_framework import serializers
from rest_framework.reverse import reverse
from courses.models import Course, Module

class CourseSerializer(serializers.ModelSerializer):
    subject = serializers.SerializerMethodField()
    instructor = serializers.SerializerMethodField()
    detail_url = serializers.SerializerMethodField()
    slug = serializers.ReadOnlyField()

    class Meta:
        model = Course
        fields = [
            'subject', 
            'title',
            'image',
            'instructor',
            'slug', 
            'overview',
            'price',
            'detail_url',
        ]
    
    def get_subject(self, obj):
        return obj.subject.title
    
    def get_instructor(self, obj):
        return obj.owner.get_full_name()

    def get_detail_url(self, obj):
        request = self.context.get('request')
        if request is None:
            return None
        return reverse("public:course_detail", kwargs={"slug": obj.slug}, request=request)

class ModuleSerializer(serializers.ModelSerializer):
    slug = serializers.ReadOnlyField()

    class Meta:
        model = Module
        fields = [
            'title',
            'description',
            'slug',
        ]

class CourseModuleSerializer(serializers.ModelSerializer):
    instructor = serializers.SerializerMethodField()
    modules = ModuleSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = [
            'title',
            'overview',
            'image',
            'price',
            'instructor',
            'updated',
            'modules',
        ]
    
    def get_instructor(self, obj):
        return obj.owner.get_full_name()