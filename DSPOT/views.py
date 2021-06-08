
from django.shortcuts import render
from django.contrib.auth.models import User, auth
from App.models import Work,Carts,Saved,FollowRequest

def home(request):

    obj=User.objects.all()
    obj2=Work.objects.all()
    CValue=Carts.objects.filter(UserName=request.user).count()
    lk=Work.objects.filter(Make_Private=False).order_by('Likes').reverse()[:15]

    return render(request, 'index.html',{'obj':obj,'obj2':obj2,'CValue':CValue,'lk':lk})