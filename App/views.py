from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.conf import settings
import urllib
import json
from Account.models import LoggedInUser, Messages, Draft_Box, Reply, Profile, Reply
from App.models import FollowRequest, Work, Carts, Saved, Likes, Feedbk, Chat,FeedBack
from Payment.models import Transaction
from django.contrib.auth.decorators import login_required
from django.db.models import F
import time
from .form import WorkUpdate
from Payment.models import Transaction
import re
import wget
from django.db.models import Q

def home(request):

    return redirect('/')


def about(request):
    CValue = Carts.objects.filter(UserName=request.user).count()

    return render(request, 'about.html', {'CValue': CValue})


@login_required
def msg(request):

    if request.method == 'POST':

        username = request.POST['uname']
        subject = request.POST['sub']
        message = request.POST['msg']
        obj = Messages.objects.get_or_create(
            UserName=username, Subject=subject, Query=message)
        obj1 = Draft_Box.objects.get_or_create(
            UserName=username, Subject=subject, Query=message, Status=False)
        messages.success(request, " We Will Contact You Soon ")

    return redirect('/')


@login_required
def blog(request):
    obj = User.objects.filter(is_superuser=False)
    CValue = Carts.objects.filter(UserName=request.user).count()

    return render(request, 'blog.html', {'obj': obj, 'CValue': CValue})


@login_required
def detail(request):
    if request.method == 'POST':
        UserName = request.POST['FW']
        obj = User.objects.filter(username=UserName)
        obj1 = FollowRequest.objects.filter(
            UserName=UserName, Sender=request.user)
        obj2 = FollowRequest.objects.filter(
            Sender=UserName, Status=True).count()
        obj3 = FollowRequest.objects.filter(
            UserName=UserName, Status=True).count()
        msg1 = Chat.objects.filter(
            SenderName=request.user, ReciverName=UserName)
        msg2 = Chat.objects.filter(
            SenderName=UserName, ReciverName=request.user)
        CValue = Carts.objects.filter(UserName=request.user).count()
        post = Work.objects.filter(Your_Name=UserName).count()
    return render(request, 'AboutUser.html', {'obj': obj, 'obj1': obj1, 'obj2': obj2, 'obj3': obj3, 'CValue': CValue, 'msg1': msg1, 'msg2': msg2, 'post': post})


@login_required
def send(request):
    if request.method == 'POST':
        UserName = request.POST['FW']
        if FollowRequest.objects.filter(UserName=UserName, Sender=request.user).exists():
            messages.error(request, " Follow Request Already Sent ")
            return redirect('blog')
        else:
            FollowRequest.objects.create(
                UserName=UserName, Sender=request.user)
            messages.success(request, " Follow Request Sent ")
            return redirect('blog')


@login_required
def requests(request):
    obj = FollowRequest.objects.filter(UserName=request.user)
    CValue = Carts.objects.filter(UserName=request.user).count()
    return render(request, 'Request.html', {'obj': obj, 'CValue': CValue})


@login_required
def Accept(request):
    if request.method == 'POST':
        Sender = request.POST.get('SS')
        FollowRequest.objects.filter(
            UserName=request.user, pk=Sender).update(Status=True)
        messages.success(request, " Follow Request Accepted ")
        return redirect('requests')


@login_required
def work(request):
    
    if request.method == 'POST':

        w_form = WorkUpdate(request.POST, request.FILES)

        if w_form.is_valid():
            save = w_form.save(commit=False)
            save.Your_Name = request.user
            w_form.save()
            messages.success(request, " Your Design is Published!")
            return redirect('/')

    else:
        w_form = WorkUpdate(request.POST)

    context = {'w_form': w_form, 'CValue': Carts.objects.filter(
        UserName=request.user).count()}

    return render(request, 'work.html', context)


@login_required
def Followers(request):
    obj = FollowRequest.objects.filter(UserName=request.user)
    obj1 = User.objects.all()
    CValue = Carts.objects.filter(UserName=request.user).count()
    return render(request, 'Followers.html', {'obj': obj, 'obj1': obj1, 'CValue': CValue})


@login_required
def Following(request):

    obj = FollowRequest.objects.filter(Sender=request.user)
    obj1 = User.objects.all()
    CValue = Carts.objects.filter(UserName=request.user).count()
    return render(request, 'Following.html', {'obj': obj, 'obj1': obj1, 'CValue': CValue})


@login_required
def remove(request):
    if request.method == 'POST':
        UserName = request.POST['FW']
        FollowRequest.objects.filter(
            UserName=request.user, Sender=UserName).delete()
        obj = FollowRequest.objects.filter(UserName=request.user)
        obj1 = User.objects.all()
        CValue = Carts.objects.filter(UserName=request.user).count()
        msg = str(UserName) + " removed from your followers"
        messages.success(request, msg)
    return render(request, 'Followers.html', {'obj': obj, 'obj1': obj1, 'CValue': CValue})


@login_required
def unfollow(request):
    if request.method == 'POST':
        UserName = request.POST['FW']
        FollowRequest.objects.filter(
            UserName=UserName, Sender=request.user).delete()
        obj = FollowRequest.objects.filter(Sender=request.user)
        obj1 = User.objects.all()
        CValue = Carts.objects.filter(UserName=request.user).count()
        msg = " You Unfollow " + str(UserName)
        messages.success(request, msg)

    return render(request, 'Following.html', {'obj': obj, 'obj1': obj1, 'CValue': CValue})


@login_required
def cart(request):
    if request.method == 'POST':
        UserName = request.POST['FW']
        DN = request.POST['FI']

        if Carts.objects.filter(UserName=request.user, Creater=UserName, Design_No=DN).exists():
            messages.success(request, 'Item Already in Your Cart')
            return redirect('/')

        elif Transaction.objects.filter(made_by=request.user,Creator=UserName, Design_No=DN).exists():
            messages.success(request, 'Item Already Purchased See Your Order History')
            return redirect('/')

        else:
            Carts.objects.get_or_create(
                UserName=request.user, Creater=UserName, Design_No=DN)
            messages.success(request, 'Design Added To Cart')
        return redirect('/')


@login_required
def Save(request):
    if request.method == 'POST':
        UserName = request.POST['FW']
        DN = request.POST['FI']

        if Saved.objects.filter(UserName=request.user, Creater=UserName, Design_No=DN).exists():
            messages.success(request, 'Item Already Saved')
            return redirect('/')
        else:
            Saved.objects.get_or_create(
                UserName=request.user, Creater=UserName, Design_No=DN)
            messages.success(request, 'Design Saved')
        return redirect('/')


@login_required
def usave(request):

    obj = Saved.objects.filter(UserName=request.user)
    obj1 = Work.objects.all()
    CValue = Carts.objects.filter(UserName=request.user).count()
    return render(request, 'saved_item.html', {'obj': obj, 'obj1': obj1, 'CValue': CValue})


@login_required
def delete(request):
    if request.method == 'POST':
        DNo = request.POST['FW']
        Saved.objects.filter(UserName=request.user, Design_No=DNo).delete()
        messages.success(request, 'Design Remove From Saved')
        obj = Saved.objects.filter(UserName=request.user)
        obj1 = Work.objects.all()
        CValue = Carts.objects.filter(UserName=request.user).count()
        return render(request, 'saved_item.html', {'obj': obj, 'obj1': obj1, 'CValue': CValue})


@login_required
def cartItem(request):

    obj = Carts.objects.filter(UserName=request.user).order_by('id').reverse()
    obj1 = Work.objects.all()
    CValue = Carts.objects.filter(UserName=request.user).count()
    return render(request, 'Cart.html', {'obj': obj, 'obj1': obj1, 'CValue': CValue})


@login_required
def Cremove(request):
    if request.method == 'POST':
        DNo = request.POST['FW']
        Carts.objects.filter(UserName=request.user, Design_No=DNo).delete()
        messages.success(request, 'Design Remove From Cart')
        obj = Carts.objects.filter(
            UserName=request.user).order_by('id').reverse()
        obj1 = Work.objects.all()
        CValue = Carts.objects.filter(UserName=request.user).count()
        return render(request, 'Cart.html', {'obj': obj, 'obj1': obj1, 'CValue': CValue})


@login_required
def LKS(request):
    if request.method == 'POST':
        UserName = request.POST['FW']
        DN = request.POST['FI']

        if Likes.objects.filter(UserName=request.user, Creater=UserName, Design_No=DN).exists():
            messages.success(request, 'Design Already Liked')
            return redirect('/')
        else:
            Likes.objects.create(
                UserName=request.user, Creater=UserName, Design_No=DN)
            Work.objects.filter(id=DN, Your_Name=UserName).update(
                Likes=F('Likes')+1)
            messages.success(request, 'Design Liked')
            return redirect('/')

    return redirect('/')


def Category(request):
    if request.method == 'GET':
        query = request.GET.get('q')
        # obj1 = Work.objects.filter(Select_Region=query, Make_Private=False)
        result=Q(Select_Region__icontains=query) | Q(Your_Name__icontains=query) | Q(Price__icontains=query)
        obj1= Work.objects.filter(result).distinct()
        CValue = Carts.objects.filter(UserName=request.user).count()
        return render(request, 'Category.html', {'obj1': obj1, 'CValue': CValue})

    else:
        obj1 = Work.objects.filter(Make_Private=False)
        CValue = Carts.objects.filter(UserName=request.user).count()
        return render(request, 'Category.html', {'obj1': obj1, 'CValue': CValue})


def posts(request):

    obj1 = Work.objects.filter(Your_Name=request.user)
    CValue = Carts.objects.filter(UserName=request.user).count()
    obj = Feedbk.objects.filter(Creater=request.user).order_by('id').reverse()

    return render(request, 'Post.html', {'obj1': obj1, 'CValue': CValue, 'obj': obj})


@login_required
def feedback(request):
    if request.method == 'POST':
        UserName = request.POST['FW']
        DN = request.POST['FI']
        cm = request.POST.get('CM')
        print(cm)
        Feedbk.objects.create(UserName=request.user,
                              Creater=UserName, Design_No=DN, Comment=cm)
        messages.success(request, 'Comment Successfully')
        return redirect('/')


@login_required
def chat(request):
    if request.method == 'POST':
        RName = request.POST['chatuser']
        Msg = request.POST['msg']
        print(RName)

        Chat.objects.create(SenderName=request.user,
                            ReciverName=RName, Message=Msg)
        messages.success(request, 'Message sent Successfully')
        return redirect('blog')


@login_required
def cleartalk(request):
    if request.method == 'POST':
        RName = request.POST['chatuser']
        msg1 = Chat.objects.filter(
            SenderName=request.user, ReciverName=RName).delete()
        msg2 = Chat.objects.filter(
            SenderName=RName, ReciverName=request.user).delete()
        messages.success(request, 'Conversation Cleared!!')
        return redirect('blog')


@login_required
def makepb(request):
    if request.method == 'POST':
        D_id = request.POST['SS']
        Work.objects.filter(Your_Name=request.user,
                            id=D_id).update(Make_Private=False)
        messages.success(request, 'Design is public now!')
        obj1 = Work.objects.filter(Your_Name=request.user)
        CValue = Carts.objects.filter(UserName=request.user).count()
        obj = Feedbk.objects.filter(Creater=request.user).order_by('id').reverse()

        return render(request, 'Post.html', {'obj1': obj1, 'CValue': CValue, 'obj': obj})


@login_required
def makepv(request):
    if request.method == 'POST':
        D_id = request.POST['SS']
        Work.objects.filter(Your_Name=request.user,
                            id=D_id).update(Make_Private=True)
        messages.success(request, 'Design is private now!')
        obj1 = Work.objects.filter(Your_Name=request.user)
        CValue = Carts.objects.filter(UserName=request.user).count()
        obj = Feedbk.objects.filter(Creater=request.user).order_by('id').reverse()

        return render(request, 'Post.html', {'obj1': obj1, 'CValue': CValue, 'obj': obj})


@login_required
def psdt(request):
    if request.method == 'POST':
        D_id = request.POST['SS']
        Work.objects.filter(Your_Name=request.user, id=D_id).delete()
        messages.success(request, 'Design is Deleted!')
        obj1 = Work.objects.filter(Your_Name=request.user)
        CValue = Carts.objects.filter(UserName=request.user).count()
        obj = Feedbk.objects.filter(Creater=request.user).order_by('id').reverse()
        Carts.objects.filter(Creater=request.user).delete()

        return render(request, 'Post.html', {'obj1': obj1, 'CValue': CValue, 'obj': obj})


@login_required
def checkout(request):
    if request.method == 'POST':
        D_id = request.POST['FW']
        Item = Carts.objects.filter(UserName=request.user, Design_No=D_id)
        pp = Work.objects.filter(id=D_id)
        for i in pp:
            Price = (i.Price)

        CValue = Carts.objects.filter(UserName=request.user).count()
        img = Work.objects.all()
    return render(request, 'CheckOut.html', {'obj': Item, 'CValue': CValue, 'img': img, 'Price': Price})


@login_required
def payment(request):
    if request.method == 'POST':
        D_id = request.POST.get('Pm')
        Item = Carts.objects.filter(UserName=request.user, Design_No=D_id)
        CValue = Carts.objects.filter(UserName=request.user).count()
    return render(request, 'Payment.html', {'obj': Item, 'CValue': CValue})


@login_required
def mypurchased(request):

    Data = Transaction.objects.filter(
        made_by=request.user).order_by('id').reverse()
    Item = Work.objects.all()
    CValue = Carts.objects.filter(UserName=request.user).count()
    return render(request, 'My Order.html', {'Data': Data, 'Item': Item, 'CValue': CValue})


@login_required
def order_history(request):
    if request.method == 'POST':
        D_id = request.POST.get('OID')
        print(D_id)
        Data = Transaction.objects.filter(made_by=request.user, id=D_id)
        CValue = Carts.objects.filter(UserName=request.user).count()
        Item = Work.objects.all()

    return render(request, 'Orderhist.html', {'Data': Data, 'Item': Item, 'CValue': CValue})


@login_required
def sorder(request):

    CValue = Carts.objects.filter(UserName=request.user).count()
    Item = Work.objects.filter(Your_Name= request.user)
    Data=Transaction.objects.filter(Creator=request.user)

    return render(request, 'SellOrder.html',{'Data': Data, 'Item': Item, 'CValue': CValue})


def Testimonials(request):
    
    if request.method == 'POST':
        
        UserName= request.POST['uname']
        Name= request.POST['name']
        Email= request.POST['email']
        Message= request.POST['message']
        
        FeedBack.objects.create(UserName=UserName,Name=Name,Email=Email,Message=Message)
        messages.success(request, 'Thank You For Your Feedback!')
        
        return redirect('Testimonials')
        
    else:
        
        obj=User.objects.all()
        CValue = Carts.objects.filter(UserName=request.user).count()
        feeds = FeedBack.objects.all()
        return render(request, 'Testimonial.html',{'feeds': feeds, 'CValue': CValue,'obj':obj})