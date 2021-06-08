from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.conf import settings
User = settings.AUTH_USER_MODEL


class LoggedInUser(models.Model):
    user = models.CharField(max_length=32, null=False, blank=False)
    # Session keys are 32 characters long
    session_key = models.CharField(max_length=32, null=False, blank=False)

    def __str__(self):
        return self.user


class Messages(models.Model):
    UserName = models.CharField(max_length=50)
    Subject = models.CharField(max_length=50)
    Query = models.TextField(max_length=300)

    def __str__(self):
        return self.UserName


class Reply(models.Model):
    UserName = models.CharField(max_length=50)
    Subject = models.CharField(max_length=50, null=False, default=" ")
    Query = models.TextField(max_length=300, default=" ")
    Response = models.TextField(max_length=300)
    

    def __str__(self):
        return self.UserName


class Draft_Box(models.Model):
    UserName = models.CharField(max_length=50)
    Subject = models.CharField(max_length=50)
    Query = models.TextField(max_length=300)
    Status=models.BooleanField(default=False)
    Response = models.TextField(max_length=300,default=" ")

    def __str__(self):
        return self.UserName


class Profile(models.Model):

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=False, default='')
    Profile_Image = models.ImageField(
        upload_to='Profile_Image', default='user.jpg')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)
        img = Image.open(self.Profile_Image.path)

        if img.width > 300 or img.height > 300:
            re_size = (300, 300)
            img.thumbnail(re_size)
            img.save(self.Profile_Image.path)


