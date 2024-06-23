from django.contrib import admin
from .models import Subject, Course, Module, Content, Text, File, Image, Video

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'slug']
    prepopulated_fields = {'slug': ('title',)}

class ModuleInline(admin.StackedInline):
    model = Module

class ContentInline(admin.StackedInline):
    model = Content
    
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['id','title', 'subject', 'created', 'available']
    list_filter = ['created', 'subject']
    list_editable = ['available']
    search_fields = ['title', 'overview']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ModuleInline]

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ['id','title', 'slug']
    inlines = [ContentInline]


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ['id', 'module', 'content_type', 'object_id', 'order']

admin.site.register(Text)
admin.site.register(File)
admin.site.register(Image)

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'transcript', 'file']
    list_editable = ['transcript']