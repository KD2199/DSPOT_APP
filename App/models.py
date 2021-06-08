from django.db import models
from django.contrib.auth.models import User

from PIL import Image
from django.conf import settings
User = settings.AUTH_USER_MODEL

option= (
    ('Traditional','Traditional'),
    ('Casual', 'Casual'),
    ('Western','Western'),
    ('South','South'),
    ('Formal ','Formal '))

class FollowRequest(models.Model):
    UserName= models.CharField(max_length=50)
    Sender= models.CharField(max_length=50)
    Status= models.BooleanField(default=False)
  
    def __str__(self):
        return self.UserName

class Work(models.Model):
    

    Your_Name= models.CharField(max_length=50,null=False)
    About_Design= models.CharField(max_length=300,null=False)
    Select_Region=models.CharField(max_length=60, choices=option, default='traditional')
    Price=models.IntegerField(null=False,default=0)
    Upload_Pictures=models.FileField(upload_to='Designs',null=False)
    Make_Private=models.BooleanField(default=False)
    Likes=models.IntegerField(null=False,default=0)
  
    def __str__(self):
        return self.Your_Name


    
class Carts(models.Model):
    UserName= models.CharField(max_length=50)
    Creater= models.CharField(max_length=50)
    Design_No=models.IntegerField(null=False,default=0)
  
    def __str__(self):
        return self.UserName

class Saved(models.Model):
    UserName= models.CharField(max_length=50)
    Creater= models.CharField(max_length=50)
    Design_No=models.IntegerField(null=False,default=0)
    
  
    def __str__(self):
        return self.UserName


class Likes(models.Model):
    UserName= models.CharField(max_length=50)
    Creater= models.CharField(max_length=50)
    Design_No=models.IntegerField(null=False,default=0)
    
  
    def __str__(self):
        return self.UserName

class Feedbk(models.Model):
    UserName= models.CharField(max_length=50)
    Creater= models.CharField(max_length=50)
    Design_No=models.IntegerField(null=False,default=0)
    Comment=models.CharField(max_length=200)
    
  
    def __str__(self):
        return self.UserName

class Chat(models.Model):
    SenderName= models.CharField(max_length=50)
    ReciverName= models.CharField(max_length=50)
    Message= models.TextField(max_length=1000)
    DateTime=models.DateTimeField(auto_now=True)
  

    def __str__(self):
        return self.SenderName

class FeedBack(models.Model):
    UserName= models.CharField(max_length=50)
    Name= models.CharField(max_length=50,null=False,blank=True)
    Email= models.CharField(max_length=50)
    Message= models.TextField(max_length=1000)
  
    def __str__(self):
        return self.UserName

