from rest_framework import serializers
from rest_framework.reverse import reverse
from .models import Subject, Course, Module, Content, Text, File, Video, Image

#---------------------
# Courses Serializers
#---------------------
class ManageCourseSerializer(serializers.ModelSerializer):
    slug = serializers.ReadOnlyField()
    create_url = serializers.SerializerMethodField(read_only=True)
    edit_url = serializers.SerializerMethodField(read_only=True)
    delete_url = serializers.SerializerMethodField(read_only=True)
    modules_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Course
        fields = [
            'subject', 
            'title',
            'slug', 
            'overview',
            'create_url',
            'edit_url',
            'delete_url',
            'modules_url',
        ]

    def get_create_url(self, obj):
        request = self.context.get('request')
        if request is None:
            return None
        return reverse("courses:course_create", request=request)
    
    def get_edit_url(self, obj):
        request = self.context.get('request')
        if request is None:
            return None
        return reverse("courses:course_edit", kwargs={"slug": obj.slug}, request=request)
    
    def get_delete_url(self, obj):
        request = self.context.get('request')
        if request is None:
            return None
        return reverse("courses:course_delete", kwargs={"slug": obj.slug}, request=request)
    
    def get_modules_url(self, obj):
        request = self.context.get('request')
        if request is None:
            return None
        return reverse("courses:manage_course_modules_list", kwargs={"slug": obj.slug}, request=request)

class CourseSerializer(serializers.ModelSerializer):
    slug = serializers.ReadOnlyField()

    class Meta:
        model = Course
        fields = [
            'subject', 
            'title',
            'slug', 
            'overview',
        ]


#---------------------
# Modules Serializers
#---------------------
class ManageModuleSerializer(serializers.ModelSerializer):
    slug = serializers.ReadOnlyField()
    edit_url = serializers.SerializerMethodField(read_only=True)
    delete_url = serializers.SerializerMethodField(read_only=True)
    contents_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Module
        fields = [
            'title',
            'description',
            'slug',
            'edit_url',
            'delete_url',
            'contents_url',
        ]

    def get_edit_url(self, obj):
        request = self.context.get('request')
        if request is None:
            return None
        return reverse("courses:module_update", kwargs={"slug": obj.slug}, request=request)

    def get_delete_url(self, obj):
        request = self.context.get('request')
        if request is None:
            return None
        return reverse("courses:module_delete", kwargs={"slug": obj.slug}, request=request)
    
    def get_contents_url(self, obj):
        request = self.context.get('request')
        if request is None:
            return None
        return reverse("courses:manage_module_content_list", kwargs={"slug": obj.slug}, request=request)
    
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
    modules = ManageModuleSerializer(many=True, read_only=True)
    create_new_module_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Course
        fields = ['title', 'create_new_module_url', 'modules']
    
    def get_create_new_module_url(self, obj):
        request = self.context.get('request')
        if request is None:
            return None
        return reverse("courses:module_create", kwargs={"slug": obj.slug}, request=request)


#---------------------
# Contents Serializers
#---------------------
class TextSerializer(serializers.ModelSerializer):
    edit_url = serializers.SerializerMethodField(read_only=True)
    delete_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Text
        fields = ['title', 'content', 'edit_url', 'delete_url']
    
    def get_edit_url(self, obj):
        request = self.context.get('request')
        if request is None:
            return None
        return reverse("courses:content_update", kwargs={"uuid": obj.uuid, "model_name": "text"}, request=request)

    def get_delete_url(self, obj):
        request = self.context.get('request')
        if request is None:
            return None
        return reverse("courses:content_update", kwargs={"uuid": obj.uuid, "model_name": "text"}, request=request)
   
class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        exclude = ['id', 'owner', 'created', 'updated']

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        exclude = ['id', 'owner', 'created', 'updated']

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        exclude = ['id', 'owner', 'created', 'updated']

class ManageContentSerializer(serializers.ModelSerializer):
    item = serializers.SerializerMethodField()

    class Meta:
        model = Content
        fields = ['item']
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        item_data = representation['item']
        model_name = instance.item.__class__.__name__.lower()
        return {model_name: item_data}
    
    def get_item(self, obj):
        item = obj.item
        model_name = item.__class__.__name__.lower()
        serializer_class = None

        if model_name == 'text':
            serializer_class = TextSerializer
        elif model_name == 'video':
            serializer_class = VideoSerializer
        elif model_name == 'image':
            serializer_class = ImageSerializer
        elif model_name == 'file':
            serializer_class = FileSerializer
        else:
            return None
        # Serialize the object using the chosen serializer
        serializer = serializer_class(instance=item)
        return serializer.data

class ModuleContentSerializer(serializers.ModelSerializer):
    contents = ManageContentSerializer(many=True, read_only=True)
    add_text_url = serializers.SerializerMethodField(read_only=True)
    add_file_url = serializers.SerializerMethodField(read_only=True)
    add_image_url = serializers.SerializerMethodField(read_only=True)
    add_video_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Module
        fields = [
            'title',
            'add_text_url',
            'add_file_url',
            'add_image_url',
            'add_video_url',
            'contents',
        ]
    
    def get_add_text_url(self, obj):
        request = self.context.get('request')
        if request is None:
            return None
        return reverse("courses:module_content_create", kwargs={"slug": obj.slug, "model_name": "text"}, request=request)
        
    def get_add_file_url(self, obj):
        request = self.context.get('request')
        if request is None:
            return None
        return reverse("courses:module_content_create", kwargs={"slug": obj.slug, "model_name": "file"}, request=request)
        
    def get_add_image_url(self, obj):
        request = self.context.get('request')
        if request is None:
            return None
        return reverse("courses:module_content_create", kwargs={"slug": obj.slug, "model_name": "image"}, request=request)
        
    def get_add_video_url(self, obj):
        request = self.context.get('request')
        if request is None:
            return None
        return reverse("courses:module_content_create", kwargs={"slug": obj.slug, "model_name": "video"}, request=request)
    