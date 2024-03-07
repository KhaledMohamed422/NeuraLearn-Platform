from rest_framework import serializers
from courses.models import Course, Module, Text, File, Image, Video

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
        fields = ['title', 'url']

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

class ModuleSerializer(serializers.ModelSerializer):
    contents = serializers.SerializerMethodField()

    class Meta:
        model = Module
        fields = [
            'order',
            'title',
            'description',
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
    title = serializers.CharField(read_only=True)
    module = ModuleSerializer(many=False, read_only=True)

    class Meta:
        model = Course
        fields = [
            'title',
            'module',
        ]