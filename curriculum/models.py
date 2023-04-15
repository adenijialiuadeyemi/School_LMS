from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.

class Standard(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(null=True, blank=True)
    description = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Subject(models.Model):
    subject_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    slug = models.SlugField(blank=True, null=True)
    standard = models.ForeignKey(Standard, on_delete=models.CASCADE, related_name="subjects")
    image = models.ImageField(upload_to="Subject_Images", blank=True)
    description = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name+"-"+self.subject_id)
        super().save(*args, **kwargs)


class Lesson(models.Model):
    lesson_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=150)
    slug = models.SlugField(blank=True, null=True)
    standard = models.ForeignKey(Standard, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="lessons")
    position = models.PositiveIntegerField(verbose_name="Chapter number")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    videos = models.FileField(upload_to="Videos", verbose_name="Videos", blank=True)
    ppt = models.FileField(upload_to="PPT", verbose_name="presentation", blank=True)
    Notes = models.FileField(upload_to="Notes", verbose_name="Notes", blank=True)

    class Meta:
        ordering = ['position']

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('curriculum:lesson_list', kwargs={'standard': self.standard.slug, 'slug': self.subject.slug})
    

class Comment(models.Model):
    lesson_name = models.ForeignKey(Lesson, null=True, on_delete=models.CASCADE, related_name='comments')
    comm_name = models.CharField(max_length=100, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField(max_length=500)
    date_added = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.comm_name = slugify("comment by" + "-" + str(self.author) + " " + str(self.date_added))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.comm_name
    
    class Meta:
        ordering = ['-date_added']

class Reply(models.Model):
    comment_name = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies')
    reply_body = models.TextField(max_length=500)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "reply to " + str(self.comment_name.comm_name)