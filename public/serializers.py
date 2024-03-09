from rest_framework import serializers
from rest_framework.reverse import reverse
from courses.models import Course, Module, Text, Image, File, Video

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

class TextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Text
        fields = ['title']
    
class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['title']

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['title']

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['title']

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


class ModuleSerializer(serializers.ModelSerializer):
    contents = serializers.SerializerMethodField()
    slug = serializers.ReadOnlyField()

    class Meta:
        model = Module
        fields = [
            'title',
            'description',
            'slug',
            'contents',
        ]

    def get_contents(self, obj):
        data = []
        request = self.context.get('request')
        for content in obj.contents.all():
            item = content.item
            data.append(ItemBaseSerializer(item, context={'request': request}).data)
        return data

class CourseModuleSerializer(serializers.ModelSerializer):
    instructor = serializers.SerializerMethodField()
    enrollments = serializers.SerializerMethodField()
    modules = ModuleSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = [
            'title',
            'overview',
            'image',
            'price',
            'instructor',
            'enrollments',
            'updated',
            'modules',
        ]
    
    def get_instructor(self, obj):
        return obj.owner.get_full_name()
    
    def get_enrollments(self, obj):
        return obj.students.count()