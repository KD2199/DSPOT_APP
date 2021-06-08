from django.shortcuts import render
from django.template import loader
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.conf import settings
import urllib
import json
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
import reportlab
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from datetime import datetime
from validate_email import validate_email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from Account.models import LoggedInUser, Draft_Box, Messages, Reply, Profile
from App.models import FollowRequest, Work, Saved, Carts
from Payment.models import Transaction
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from sendsms.message import SmsMessage
from sendsms import api
import string
import random
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from .form import ProfileUpdate, UserUpdateForm
from django.shortcuts import render
from django.contrib.auth import authenticate, login as auth_login
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .tokens import account_activation_token
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import get_user_model

def register(request):

    if request.method == 'POST':

        Fname = request.POST['fname']
        Lname = request.POST['lname']
        password = request.POST['password']
        password2 = request.POST['pw2']
        email = request.POST['email']
        last_name = request.POST['pp']
        
        print(email)

        if password == password2:

            if User.objects.filter(email=email).exists():
                messages.error(request, "* Email is already registered")

            else:

                is_valid = validate_email(email, verify=True)
                print(is_valid)
                
                if is_valid == True:

                    N = 4
                    VC = ''.join(random.choices(string.ascii_uppercase +
                                                string.digits, k=N))

                    first_name = Fname[0]+Lname[0]+VC

                    user = User.objects.create_user(
                        username=Fname+" "+Lname, first_name=first_name, last_name=last_name, email=email, password=password,is_active = False)
                    user.save()

                    current_site = get_current_site(request)
                    html_message = loader.render_to_string(
                        'email.html',
                        {
                            'user_name':first_name,
                            'password':  password,
                            'user': user,
                            'domain': current_site.domain,
                            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                            'token': account_activation_token.make_token(user),
                        }
                    )

                    subject = 'Verify & Activate your account.'
                    message = 'Your Registration is Successfully Completed!!'+'\n\nYour Username : ' + \
                        first_name+'\nYour Password : '+password+'\n\nThanks & Regards,\nD-SPOT TEAM'
                    email_from = settings.EMAIL_HOST_USER

                    recipient_list = [email, ]
                    send_mail(subject, message, email_from,
                              recipient_list, fail_silently=False,html_message=html_message)
                    print('Confirmation email sent!!')
                
                    messages.success(
                        request, " Registration Successfully Check Mail For Verification and Credential!")

                else:
                    messages.error(
                        request, " You Have Entered InValid Email Address. Please Verify It. ")

        else:
            messages.error(
                request, " Password & Confirm Password Didn't Matched! ")

    return redirect('/')

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(
                request, " Your Account is verified. Now you can login your account. ")
        return redirect('/')
    else:
        messages.success(
                request, " Activation link is invalid!")
        return redirect('/')


def login(request):

    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':

        try:

            recaptcha_response = request.POST.get('g-recaptcha-response')
            url = 'https://www.google.com/recaptcha/api/siteverify'
            values = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            data = urllib.parse.urlencode(values).encode()
            req = urllib.request.Request(url, data=data)
            response = urllib.request.urlopen(req)
            result = json.loads(response.read().decode())

            if result['success']:
                print("recaptcha validation successfully")
                username = request.POST['username']
                password = request.POST['password']

                obj = User.objects.filter(first_name=username)
                for i in obj:
                    email = i.email
                    user = i.username
                    status=i.is_active
                     
                if (status == True):
                    
                    user = auth.authenticate(username=user, password=password)
                    
                    if user is not None:
                        auth.login(request, user)
                        messages.success(request, " Login Successfully ")
                        return redirect('/')
                
                    else:
                        messages.error(
                            request, " You Have Entered Invalid Username or Password ")
                        return redirect('/')
                else:
                    messages.error(
                        request, " Your Account is not activated. Please verified your account.")
                    return redirect('/')

            else:
                messages.error(
                    request, " Captcaha Validation Failed Please Try Again! ")
            return redirect('/')

        except:

            messages.error(
                request, " Something Went Wrong Please Try Again! ")
            return redirect('/')

    return redirect('/')


def VC(request):
    if request.method == 'POST':

        C1 = request.POST.get('c1')
        C2 = request.POST.get('c2')
        username = request.POST.get('username')
        password = request.POST.get('password')
        if C1 == C2:
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                messages.success(request, " Login Successfully ")
                return redirect('/')
        else:
            messages.error(
                request, " SecretCode Verification Failed! ")
            return redirect('/')

    return redirect('/')


def logout(request):
    LoggedInUser.objects.filter(user=request.user).delete()
    auth.logout(request)
    messages.success(request, " Logout Successfully ")
    return redirect('/')


@login_required
def profile(request):

    uname = request.user
    obj = Draft_Box.objects.filter(UserName=uname).count()
    obj3 = Reply.objects.filter(UserName=uname).count()
    obj4 = Profile.objects.filter(user=uname)
    obj1 = FollowRequest.objects.filter(Sender=uname, Status=True).count()
    obj2 = FollowRequest.objects.filter(UserName=uname, Status=True).count()
    obj5 = Work.objects.filter(Your_Name=uname).count()
    sv = Saved.objects.filter(UserName=request.user).count()
    CValue = Carts.objects.filter(UserName=request.user).count()

    return render(request, 'profile.html', {'obj': obj, 'obj3': obj3, 'obj4': obj4, 'obj1': obj1, 'obj2': obj2, 'obj5': obj5, 'sv': sv, 'CValue': CValue})


@login_required
def Aprofile(request):
    uname = request.user
    obj1 = User.objects.all().count()-1

    return render(request, 'profile.html', {'obj1': obj1})


@login_required
def pupdate(request):

    if request.method == 'POST':

        # u_form = UserUpdateForm(request.POST,instance=request.user)
        p_form = ProfileUpdate(request.POST, request.FILES,
                               instance=request.user.profile)

        if p_form.is_valid():
            # u_form.save()
            p_form.save()
            messages.success(request, " Profile Update Successfully ")
            uname = request.user
            obj = Draft_Box.objects.filter(UserName=uname).count()
            obj3 = Reply.objects.filter(UserName=uname).count()
            obj4 = Profile.objects.filter(user=uname)
            obj1 = FollowRequest.objects.filter(
                Sender=uname, Status=True).count()
            obj2 = FollowRequest.objects.filter(
                UserName=uname, Status=True).count()
            obj5 = Work.objects.filter(Your_Name=uname).count()
            sv = Saved.objects.filter(UserName=request.user).count()
            CValue = Carts.objects.filter(UserName=request.user).count()

            return render(request, 'profile.html', {'obj': obj, 'obj3': obj3, 'obj4': obj4, 'obj1': obj1, 'obj2': obj2, 'obj5': obj5, 'sv': sv, 'CValue': CValue})

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdate(instance=request.user.profile)

    context = {'p_form': p_form, 'u_form': u_form, 'CValue': Carts.objects.filter(
        UserName=request.user).count()}

    return render(request, 'updateprofile.html', context)


@login_required
def Inbox(request):

    obj = Reply.objects.filter(UserName=request.user)
    CValue = Carts.objects.filter(UserName=request.user).count()

    return render(request, 'msg.html', {'obj': obj, 'CValue': CValue})


@login_required
def msg(request):

    obj = Draft_Box.objects.all()

    if request.method == 'POST':
        Pk = request.POST.get('key')
        username = request.POST.get('U')
        Response = request.POST['msg']
        Subject = request.POST['S']
        Query = request.POST['Q']
        obj1 = Reply.objects.get_or_create(
            UserName=username, Subject=Subject, Query=Query, Response=Response)
        Messages.objects.filter(pk=Pk).delete()
        Draft_Box.objects.filter(pk=Pk).update(Status=True, Response=Response)
        obj = Draft_Box.objects.all()
        messages.success(request, " Reply sent Successfully ")
        return render(request, 'amsg.html', {'obj': obj})

    return render(request, 'amsg.html', {'obj': obj})


@login_required
def delete(request):

    User.objects.filter(username=request.user).delete()
    Saved.objects.filter(UserName=request.user).delete()
    Carts.objects.filter(UserName=request.user).delete()
    Work.objects.filter(Your_Name=request.user).delete()
    FollowRequest.objects.filter(UserName=request.user).delete()
    FollowRequest.objects.filter(Sender=request.user).delete()
    Draft_Box.objects.filter(UserName=request.user).delete()
    Reply.objects.filter(UserName=request.user).delete()
    LoggedInUser.objects.filter(user=request.user).delete()
    Transaction.objects.filter(Creator=request.user)
    messages.success(request, " Account Delete Successfully ")
    return redirect('/')