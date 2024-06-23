from rest_framework import serializers
from rest_framework.reverse import reverse
from .models import Subject, Course, Module, Content, Text, File, Video, Image
from drf_spectacular.utils import extend_schema_field

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'title', 'slug', 'image']
    
#---------------------
# Courses Serializers
#---------------------
class CourseSerializer(serializers.ModelSerializer):
    slug = serializers.ReadOnlyField()

    class Meta:
        model = Course
        fields = [
            'subject', 
            'title',
            'slug', 
            'overview',
            'price',
            'image',
        ]

class ManageCourseSerializer(serializers.ModelSerializer):
    subject = serializers.StringRelatedField()
    slug = serializers.ReadOnlyField()
    detail_url = serializers.SerializerMethodField(read_only=True)
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
            'price',
            'image',
            'created',
            'updated',
            'detail_url',
            'edit_url',
            'delete_url',
            'modules_url',
        ]
    
    @extend_schema_field(str)
    def get_detail_url(self, obj):
        request = self.context.get('request')
        if request is None:
            return None
        return reverse("courses:manage_course_detail", kwargs={"slug": obj.slug}, request=request)

    @extend_schema_field(str)
    def get_edit_url(self, obj):
        request = self.context.get('request')
        if request is None:
            return None
        return reverse("courses:course_edit", kwargs={"slug": obj.slug}, request=request)
    
    @extend_schema_field(str)
    def get_delete_url(self, obj):
        request = self.context.get('request')
        if request is None:
            return None
        return reverse("courses:course_delete", kwargs={"slug": obj.slug}, request=request)
    
    @extend_schema_field(str)
    def get_modules_url(self, obj):
        request = self.context.get('request')
        if request is None:
            return None
        return reverse("courses:manage_course_modules_list", kwargs={"slug": obj.slug}, request=request)

class CourseDetailSerializer(serializers.ModelSerializer):
    subject = serializers.StringRelatedField()
    slug = serializers.ReadOnlyField()
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
            'price',
            'image',
            'created',
            'updated',
            'edit_url',
            'delete_url',
            'modules_url',
        ]

    @extend_schema_field(str)
    def get_edit_url(self, obj):
        request = self.context.get('request')
        if request is None:
            return None
        return reverse("courses:course_edit", kwargs={"slug": obj.slug}, request=request)
    
    @extend_schema_field(str)
    def get_delete_url(self, obj):
        request = self.context.get('request')
        if request is None:
            return None
        return reverse("courses:course_delete", kwargs={"slug": obj.slug}, request=request)
    
    @extend_schema_field(str)
    def get_modules_url(self, obj):
        request = self.context.get('request')
        if request is None:
            return None
        return reverse("courses:manage_course_modules_list", kwargs={"slug": obj.slug}, request=request)

class CourseAvailableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'title', 'available']

        
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

    @extend_schema_field(str)
    def get_edit_url(self, obj):
        request = self.context.get('request')
        if request is None:
            return None
        return reverse("courses:module_update", kwargs={"slug": obj.slug}, request=request)
    
    @extend_schema_field(str)
    def get_delete_url(self, obj):
        request = self.context.get('request')
        if request is None:
            return None
        return reverse("courses:module_delete", kwargs={"slug": obj.slug}, request=request)
    
    @extend_schema_field(str)
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
    
    @extend_schema_field(str)
    def get_create_new_module_url(self, obj):
        request = self.context.get('request')
        if request is None:
            return None
        return reverse("courses:module_create", kwargs={"slug": obj.slug}, request=request)


#---------------------
# Contents Serializers
#---------------------
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

class ManageContentSerializer(serializers.ModelSerializer):
    item = serializers.SerializerMethodField()
    
    class Meta:
        model = Content
        fields = ['item']
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        item_data = representation['item']
        model_name = instance.item.__class__.__name__.lower()
        return { model_name: item_data }
    
    def get_item(self, obj) -> dict:
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
        request = self.context.get('request')
        serializer = serializer_class(instance=item, context={"request": request})
        serializer_data = dict(serializer.data)
        serializer_data["edit_url"] = self.get_edit_url(obj)
        serializer_data["delete_url"] = self.get_delete_url(obj)
        return serializer_data

    def get_edit_url(self, obj):
        request = self.context.get('request')
        model_name = obj.item.__class__.__name__.lower()
        if request is None:
            return None
        return reverse(f"courses:content_{model_name}_update_delete", kwargs={"id": obj.id}, request=request)

    def get_delete_url(self, obj):
        request = self.context.get('request')
        model_name = obj.item.__class__.__name__.lower()
        if request is None:
            return None
        return reverse(f"courses:content_{model_name}_update_delete", kwargs={"id": obj.id}, request=request)
 

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
    
    @extend_schema_field(str)
    def get_add_text_url(self, obj):
        request = self.context.get('request')
        if request is None:
            return None
        return reverse("courses:module_content_text_create", kwargs={"slug": obj.slug}, request=request)

    @extend_schema_field(str)   
    def get_add_file_url(self, obj):
        request = self.context.get('request')
        if request is None:
            return None
        return reverse("courses:module_content_file_create", kwargs={"slug": obj.slug}, request=request)
    
    @extend_schema_field(str)   
    def get_add_image_url(self, obj):
        request = self.context.get('request')
        if request is None:
            return None
        return reverse("courses:module_content_image_create", kwargs={"slug": obj.slug}, request=request)

    @extend_schema_field(str)   
    def get_add_video_url(self, obj):
        request = self.context.get('request')
        if request is None:
            return None
        return reverse("courses:module_content_video_create", kwargs={"slug": obj.slug}, request=request)
    