from django.contrib import admin
from .models import userProfileInfo
# Register your models here.

@admin.register(userProfileInfo)
class userProfileInfoAdmin(admin.ModelAdmin):
    pass
