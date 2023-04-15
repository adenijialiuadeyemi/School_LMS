from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class userProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=150, blank=True)
    profile_pics = models.ImageField(upload_to='profile_images/', verbose_name="profile picture", blank=True)
    user_types = [('Teacher','Teacher'), ('Student','Student'), ('Parent','Parent')]
    user_type = models.CharField(max_length=10, choices=user_types, default="Student")

    def __str__(self):
        return self.user.username


    
