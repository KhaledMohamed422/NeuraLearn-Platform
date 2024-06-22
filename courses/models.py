import uuid
from django.db import models
from users.models import UserAccount as User 
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.text import slugify
from django.core.validators import FileExtensionValidator
from .utils import unique_slug_generator
from .fields import OrderField

class Subject(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField(upload_to='subjects/%Y/%m/%d/', blank=True)

    class Meta:
        ordering = ['title']

    def get_total_courses(self):
        return self.courses.count()
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug_generator(self)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title

class Course(models.Model):
    owner = models.ForeignKey(User,
                           related_name='courses_created',
                           on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject,
                                related_name='courses',
                                on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    overview = models.TextField(max_length=5000)
    students = models.ManyToManyField(User,
                                  related_name='courses_joined',
                                  blank=True)
    image = models.ImageField(upload_to='courses/%Y/%m/%d/', blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    available = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['title'])
        ]

    def get_total_modules(self):
        return self.modules.count()
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug_generator(self)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Module(models.Model):
    course = models.ForeignKey(Course,
                               related_name='modules',
                               on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(max_length=5000, blank=True)
    order = OrderField(blank=True, for_fields=['course'])

    class Meta:
        ordering = ['order']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug_generator(self)
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f'{self.order}. {self.title}'

class Content(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    module = models.ForeignKey(Module,
                               related_name='contents',
                               on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType,
                               on_delete=models.CASCADE,
                               limit_choices_to={'model__in':(
                                                'text',
                                                'video',
                                                'image',
                                                'file')})
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')
    order = OrderField(blank=True, for_fields=['module'])

    class Meta:
        ordering = ['order']

class ItemBase(models.Model):
    owner = models.ForeignKey(User,
                         related_name='%(class)s_related',
                         on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
    
    def __str__(self):
        return self.title
    
class Text(ItemBase):
    content = models.TextField(max_length=5000)

class File(ItemBase):
    file = models.FileField(upload_to='files/%Y/%m/%d/',
                            validators=[FileExtensionValidator(['pdf'])])

class Image(ItemBase):
    file = models.ImageField(upload_to='images/%Y/%m/%d/')

class Video(ItemBase):
    file = models.FileField(upload_to='videos/%Y/%m/%d/',
                            validators=[FileExtensionValidator(['mp4'])])
    transcript = models.TextField(null=True, blank=True)
    summariztion = models.TextField(null=True, blank=True)