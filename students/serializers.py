from rest_framework import serializers
from rest_framework.reverse import reverse
from drf_spectacular.utils import extend_schema_field
from courses.models import Course, Module, Text, File, Image, Video
from typing import List

class StudentCourseSerializer(serializers.ModelSerializer):
    subject = serializers.SerializerMethodField()
    instructor = serializers.SerializerMethodField()
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
        ]

    def get_subject(self, obj) -> str:
        return obj.subject.title
    
    def get_instructor(self, obj) -> str:
        return obj.owner.get_full_name()
    
class TextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Text
        fields = ['title', 'content']
    
class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['title', 'file']

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['title', 'file']

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['title', 'file']

class ItemBaseSerializer(serializers.Serializer):
    def to_representation(self, instance):
        model_name = instance._meta.model_name
        request = self.context.get('request')
        if model_name == "text":
            return {
                "text": TextSerializer(instance, context={"request": request}).data
            }
        elif model_name == "file":
            return {
                "file": FileSerializer(instance, context={"request": request}).data
            }
        elif model_name == "image":
            return {
                "image": ImageSerializer(instance, context={"request": request}).data
            }
        elif model_name == "video":
            return {
                "video":VideoSerializer(instance, context={"request": request}).data
            }

class StudentModulesSerializer(serializers.ModelSerializer):
    contents_url = serializers.SerializerMethodField()

    class Meta:
        model = Module
        fields = [
            'order',
            'title',
            'slug',
            'description',
            'contents_url',
        ]
    
    def get_contents_url(self, obj) -> str:
        request = self.context.get('request')
        if request is None:
            return None
        return reverse("students:student_module_content_list", kwargs={"slug": obj.slug}, request=request)

class StudentModuleSerializer(serializers.ModelSerializer):
    contents = serializers.SerializerMethodField()

    class Meta:
        model = Module
        fields = [
            'title',
            'description',
            'slug',
            'contents'
        ]

    def get_contents(self, obj) -> List[dict]:
        data = []
        request = self.context.get('request')
        for content in obj.contents.all():
            item = content.item
            data.append(ItemBaseSerializer(item, context={'request': request}).data)
        return data

class StudentCourseModulesSerializer(serializers.ModelSerializer):
    title = serializers.CharField(read_only=True)
    modules = StudentModulesSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = [
            'title',
            'modules',
        ]

"""
contents = serializers.SerializerMethodField()

"""