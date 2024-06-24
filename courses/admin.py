from django.contrib import admin
from .models import Subject, Course, Module, Content, Text, File, Image, Video

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'slug']
    prepopulated_fields = {'slug': ('title',)}

class TextInline(admin.StackedInline):
    model = Text

class FileInline(admin.StackedInline):
    model = File

class ImageInline(admin.StackedInline):
    model = Image

class VideoInline(admin.StackedInline):
    model = Video

class ContentInline(admin.StackedInline):
    model = Content

class ModuleInline(admin.StackedInline):
    model = Module
    inlines = [ContentInline, TextInline, FileInline, ImageInline, VideoInline]

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'slug', 'subject', 'created', 'available']
    list_filter = ['created', 'subject']
    list_editable = ['available']
    search_fields = ['title', 'overview']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ModuleInline]

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'slug']
    inlines = [ContentInline, TextInline, FileInline, ImageInline, VideoInline]

@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ['id', 'module', 'content_type', 'object_id']

@admin.register(Text)
class TextAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'content', 'owner']

@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'file', 'owner']

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'file', 'owner']

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'transcript', 'file']
    list_editable = ['transcript']
