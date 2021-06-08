from django.shortcuts import render
from django.contrib.auth import authenticate, login as auth_login
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import Transaction
from .Paytm import generate_checksum, verify_checksum
from django.contrib.auth.decorators import login_required
from App.models import FollowRequest, Work, Carts, Saved, Likes, Feedbk, Chat
from django.contrib.auth.models import User, auth


@login_required
def initiate_payment(request, Did):
    if request.method == "GET":
        return render(request, 'pay.html')
    try:
        username = request.POST['username']
        password = request.POST['password']
        temp= User.objects.filter(first_name=username)
        
        for i in temp:
            username=i
        user = authenticate(request, username=username, password=password)

        if user is None:
            raise ValueError
        auth_login(request=request, user=user)
    except:
        return render(request, 'pay.html')

    Data = Carts.objects.filter(UserName=request.user, Design_No=Did)

    pp = Work.objects.filter(id=Did)
    for i in pp:
        Price=(i.Price)
        name=(i.Your_Name)
    transaction = Transaction.objects.create(made_by=user, amount=Price,Design_No=Did,Creator=name)
    transaction.save()
    Carts.objects.filter(UserName=request.user,Design_No=Did).delete()
    merchant_key = settings.PAYTM_SECRET_KEY

    params = (
        ('MID', settings.PAYTM_MERCHANT_ID),
        ('ORDER_ID', str(transaction.order_id)),
        ('CUST_ID', str(transaction.made_by.email)),
        ('TXN_AMOUNT', str(transaction.amount)),
        ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
        ('WEBSITE', settings.PAYTM_WEBSITE),
        # ('EMAIL', request.user.email),
        # ('MOBILE_N0', '9911223388'),
        ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
        ('CALLBACK_URL', 'http://127.0.0.1:8000/payment/callback/'),
        # ('PAYMENT_MODE_ONLY', 'NO'),
    )

    paytm_params = dict(params)
    checksum = generate_checksum(paytm_params, merchant_key)
    
    transaction.checksum = checksum
    transaction.save()

    paytm_params['CHECKSUMHASH'] = checksum
    print('SENT: ', checksum)
    return render(request, 'redirect.html', context=paytm_params)


@csrf_exempt
def callback(request):
    if request.method == 'POST':
        paytm_checksum = ''
        print(request.body)
        print(request.POST)
        received_data = dict(request.POST)
        print(received_data)
        paytm_params = {}
        paytm_checksum = received_data['CHECKSUMHASH'][0]
        for key, value in received_data.items():
            if key == 'CHECKSUMHASH':
                paytm_checksum = value[0]
            else:
                paytm_params[key] = str(value[0])
        # Verify checksum
        is_valid_checksum = verify_checksum(paytm_params, settings.PAYTM_SECRET_KEY, str(paytm_checksum))
        if is_valid_checksum:
            print("Checksum Matched")
            received_data['message'] = "Checksum Matched"
            Transaction.objects.filter(order_id=paytm_params['ORDERID']).update(Status=str(paytm_params['STATUS']))
         
        else:
            print("Checksum Mismatched")
            received_data['message'] = "Checksum Mismatched"
            Transaction.objects.filter(order_id=paytm_params['ORDERID']).update(Status=str(paytm_params['STATUS']))

        return render(request, 'callback.html', context=received_data)
