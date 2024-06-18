from django.contrib import admin
from .models import Subject, Course, Module, Content, Text, File, Image, Video

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'slug']
    prepopulated_fields = {'slug': ('title',)}

class ModuleInline(admin.StackedInline):
    model = Module
    
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['id','title', 'subject', 'created', 'available']
    list_filter = ['created', 'subject']
    list_editable = ['available']
    search_fields = ['title', 'overview']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ModuleInline]

admin.site.register(Module)
admin.site.register(Content)
admin.site.register(Text)
admin.site.register(File)
admin.site.register(Image)

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'transcript']
    list_editable = ['transcript']