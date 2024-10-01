from django.shortcuts import render,redirect
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core.mail import send_mail
from bitcoin import *
from django.conf import settings
from payments.models import *
import requests
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth import update_session_auth_hash
from .models import *
from .forms import *
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required
from payments.models import *
import pyotp
from .utils import *
from django.utils.timezone import  timedelta
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.db.models import Q, Sum
from rest_framework.decorators import api_view
from rest_framework.response import Response 
from rest_framework import status
from decimal import Decimal

User = get_user_model()

@login_required(login_url = 'sign_in')
def edit_profile(request):
    instance = get_object_or_404(Account, username=request.user.username)
    if request.method == 'POST':
            
        # user_form = UserForm(request.POST, request.FILES, instance=request.user)
        
        # if user_form.is_valid():
        #     user_form.save()
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        state = request.POST.get('state')
        btc_addr = request.POST.get('btc_addr')
        instance.first_name = first_name
        instance.last_name = last_name
        instance.username = username
        instance.state = state
        instance.bitcoin_address = btc_addr
        instance.save()    
        messages.success(request, 'Your profile has been updated.')
        return redirect('/edit_profile')
    else:
        user_form = UserForm(instance=request.user)
        
    context = {
        'user_form':user_form,   
    }
    return render(request, 'crypto/dashboard/profile.html', context)
    

def sign_up(request, referred='',bot=''):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
    else:
        if request.method == 'POST':
            try:
                bot = request.POST.get('bot-c')
                if bot == '':
                    pass
                else:
                    return redirect('/sign_up')
            except Account.DoesNotExist:
                pass
                        
            username = request.POST['username']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            country = request.POST['country']
            phone = request.POST['phone']
            password = request.POST['password']
            confirm_password = request.POST['confirm_password']
          
                    
            if Account.objects.filter(username=username).exists():
                messages.warning(request, 'Username already exists')
                return redirect('/sign_up')
            if Account.objects.filter(email=email).exists():
                messages.warning(request, 'Email already exists')
                return redirect('/sign_up')
            if Account.objects.filter(email=email, is_active=False).exists():
                messages.warning(request, 'Email already exists, Please verify your mail')
                return redirect('/sign_up')
            if password != confirm_password:
                messages.warning(request, "Password does not match with the confirm password!")
                return redirect('/sign_up')
            if len(password) < 8:
                messages.warning(request, "Password too weak! It must be at least 8 characters long.")
                return redirect('/sign_up')       
            user = Account.objects.create_user(first_name=first_name,last_name=last_name,email=email,username=username,password=password)
            try:
                code = request.POST.get('ref_code')
                if not code:
                    code = request.session.get('ref_code')
                    print(code)
                if code:
                    referrer = Account.objects.get(code=code)
                    Referral.objects.create(referrer=referrer, referred=user)
                    
                    # mail_subject_referrer = 'New Referral Sign-up'
                    # message_referrer = f'The user {user.email} signed up using your referral code.'
                    # send_mail(mail_subject_referrer, message_referrer, settings.DEFAULT_FROM_EMAIL, [referrer.email], fail_silently=False)
                    
                    # referrer.crypto_balance += Decimal(5)
                    referrer.save()
                    del request.session['ref_code']
                else:
                    pass
            except Account.DoesNotExist:
                messages.warning(request, "Referral code does not exist")
                return redirect('/sign_up')
            
            user.country=country
            user.phone=phone
            # otp = generate_otp()
            # user.otp = otp
            # user.otp_created_at = timezone.now()
            # send_otp_via_email(email, otp)
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Welcome To TradewithKennellysi'
            message = render_to_string('trade/account/account_welcome_email.html', {
                'user' : user,
                'domain' : current_site,
                # 'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
                # 'token' : default_token_generator.make_token(user)
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.content_subtype = "html"
            send_email.send()

            # send_mail('New Sign up','Email ' + email + ' Username: '+username,settings.DEFAULT_FROM_EMAIL,[settings.DEFAULT_FROM_EMAIL],fail_silently=False)
            
            messages.success(request, 'Congratulations! Your account is activated.')

            return redirect('/sign_in')      
        else:      
            return render(request, 'trade/account/signup.html', {})

# def otp_view(request):
#     if request.method == 'POST':
#         otp = request.POST['otp']
#         email = request.POST['email']
#         # email = request.session['email']
#         try:
#             user = User.objects.get(email=email, otp=otp)
#             if user.otp_created_at + timedelta(minutes=10) < timezone.now(): #checks expiry duration
#                 messages.error(request,'OTP expired')
#                 return render(request, 'crypto/auth/otp.html', {})
#             user.is_active = True
#             user.otp = None
#             user.otp_created_at = None
#             user.save()
#             current_site = get_current_site(request)
#             mail_subject = 'Welcome To CARAXASSET'
#             message = render_to_string('crypto/auth/account_welcome_email.html', {
#                 'user' : user,
#                 'domain' : current_site,
#                 # 'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
#                 # 'token' : default_token_generator.make_token(user)
#             })
#             to_email = email
#             send_email = EmailMessage(mail_subject, message, to=[to_email])
#             send_email.content_subtype = "html"
#             send_email.send()
#             return redirect('/sign_in')
#         except User.DoesNotExist:
#             messages.error(request,'OTP Invalid')
#             return render(request, 'crypto/auth/otp.html', {})
#     return render(request, 'crypto/auth/otp.html')


# def activate(request, uidb64, token):
#     try:
#         uid = urlsafe_base64_decode(uidb64).decode()
#         user = Account._default_manager.get(pk=uid)
#     except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
#         user = None

#     if user is not None and default_token_generator.check_token(user, token):
#         user.is_active = True
#         user.save()
#         messages.success(request, 'Congratulations! Your account is activated.')
#         return redirect('/sign_in')
#     else:
#         messages.error(request, 'Invalid activation link')
#         return redirect('/sign_up')

def sign_in(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('dashboard')
    else:
        if request.method == 'POST':
            credential = request.POST['username_or_email']  # Accept either email or username
            password = request.POST['password']

            User = get_user_model()

            if '@' in credential:
                # Assume it's an email
                try:
                    user = User.objects.get(email=credential)
                except User.DoesNotExist:
                    user = None
            else:
                # Assume it's a username
                try:
                    user = User.objects.get(username=credential)
                except User.DoesNotExist:
                    user = None

            if user is not None and user.check_password(password):
                auth.login(request, user)

                url = request.META.get('HTTP_REFERER')
                try:
                    query = requests.utils.urlparse(url).query
                    params = dict(x.split('=') for x in query.split('&'))
                    if 'next' in params:
                        nextpage = params['next']
                        return redirect(nextpage)
                except:
                    return HttpResponseRedirect('dashboard')
            else:
                messages.error(request, 'Invalid credentials')
                return redirect('/sign_in')
        else:
            return render(request, 'trade/account/login.html', {})

def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

@login_required(login_url = 'sign_in')
def ref(request):
    user_referrals = Referral.objects.filter(referrer=request.user)
    current_site = get_current_site(request)
    scheme = 'https' if request.is_secure() else 'http'
    referral_link = f'{scheme}://{current_site.domain}/?ref_code={request.user.code}'
    referrals = request.user.total_referrals
    total_referals = 0
    if referrals != None:
        total_referals = referrals.count()
    context={
        'referral_link':referral_link,
        'user_referrals':user_referrals,
        'total_referals':total_referals,
    }
    return render(request, "crypto/dashboard/referral-link.html",context)


@api_view(['GET','POST','PUT'])
def validate_earning(request):
    cal_d = Investment.objects.all().filter(status='Approved',added_to_balance=False)
    for inventments in cal_d:
        if inventments.plan == "RUBY PLAN":
            inventments.user.interest_wallet += Decimal(inventments.percentage)
            inventments.user.total_invest += inventments.amount
            inventments.user.save()
            inventments.added_to_balance = True
            inventments.save()
        elif inventments.plan == "CONSERVATIVE PLAN":
            inventments.user.interest_wallet += Decimal(inventments.percentage)
            inventments.user.total_invest += inventments.amount
            inventments.user.save()
            inventments.added_to_balance = True
            inventments.save()
        elif inventments.plan == "PLATINUM PLAN":
            inventments.user.interest_wallet += Decimal(inventments.percentage)
            inventments.user.total_invest += inventments.amount
            inventments.user.save()
            inventments.added_to_balance = True
            inventments.save()

    now = timezone.now()
    expired_date = now.astimezone() - timedelta(days=7)
    model_list = Investment.objects.all().filter(created_at__lt=expired_date)
    for model_item in model_list:
        if model_item.status == "Approved" and model_item.plan == 'RUBY PLAN':
            model_item.status = "Completed"
            model_item.save()
            
    now = timezone.now()
    expired_date = now - timedelta(days=7)
    model_list = Investment.objects.all().filter(created_at__lt=expired_date)
    for model_item in model_list:
        if model_item.status == "Approved" and model_item.plan == 'CONSERVATIVE PLAN':
            model_item.status = "Completed"
            model_item.save()
    
    now = timezone.now()
    expired_date = now - timedelta(days=7)
    model_list = Investment.objects.all().filter(created_at__lt=expired_date)
    for model_item in model_list:
        if model_item.status == "Approved" and model_item.plan == 'PLATINUM PLAN':
            model_item.status = "Completed"
            model_item.save()
    
    return Response({'message':'Processed Successfully'}, status=status.HTTP_202_ACCEPTED)



@login_required(login_url='sign_in')
def dashboard(request):
    user = request.user
    deposits = Investment.objects.filter(user=user).order_by("-created_at")

    # Last deposit
    last_deposit = deposits.last()

    # Total deposit amount
    total_deposit = deposits.aggregate(total=Sum('amount'))['total']
    total_deposit = total_deposit if total_deposit is not None else 0  # Handle None case
    active_deposit = deposits.filter(status='Approved').aggregate(total=Sum('amount'))['total']


    # Count total approved or completed orders
    total_orders = deposits.filter(Q(status='Approved') | Q(status='Completed')).count()

    # Count pending orders
    pending = deposits.filter(status='Pending').count()
    transactions = Transaction.objects.filter(user=user).order_by("-created_at")
    withdrawals = Crypto_Withdrawal_Request.objects.filter(user=user)
    last_withdrawal = withdrawals.last()
    pending_withdrawal = withdrawals.filter(status='Pending').aggregate(total=Sum('amount'))['total']
    context = {
        'deposits': deposits,
        'total_orders': total_orders,
        'pending': pending,
        'active_deposit':active_deposit,
        'total_deposit': total_deposit,
        'transactions': transactions,
        'last_withdrawal':last_withdrawal,
        'pending_withdrawal':pending_withdrawal,
    }
    return render(request, 'crypto/dashboard/dashboard.html', context)

@login_required(login_url = 'sign_in')
def change_password(request):
    if request.method == 'POST':
        
        current_password = request.POST['old_password']
        new_password = request.POST["new_password"]
        confirmed_new_password = request.POST["confirm_password"]
        
        if  new_password and confirmed_new_password:
            if request.user.is_authenticated:
                user = User.objects.get(username= request.user.username)
                
                if not user.check_password(current_password):
                    messages.warning(request, 'Old Password does not match')
                    return redirect('/change_password')
                elif len(new_password) < 8:
                    messages.warning(request, "Your new password must be at least 8 characters long!")
                    return redirect('/change_password')
                elif new_password != confirmed_new_password:
                    messages.warning(request, "Your new password does not match with the confirm password!")
                    return redirect('/change_password')
                else:
                    user.set_password(new_password)
                    user.save()
                    update_session_auth_hash(request, user)

                    messages.success(request, "your password has been changed successfuly.!")

                    return redirect('/change_password')

        else:
            messages.warning(request, " sorry , all fields are required !")
    return render(request, 'crypto/dashboard/change-password.html',{})



def forgetpassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)


            current_site = get_current_site(request)
            mail_subject = 'Reset your password'
            message = render_to_string('trade/account/reset_password_mail.html', {
                'user' : user,
                'domain' : current_site,
                'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
                'token' : default_token_generator.make_token(user)
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[request.POST['email']])
            send_email.content_subtype = "html"
            send_email.send()

            messages.success(request, 'Password reset email has been sent to your email address.')
            return redirect('/sign_in')

        else:
            messages.error(request, 'Account does not exists!')
            return redirect('/forgetpassword')
    return render(request, 'trade/account/forgot.html', {})


def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect('/resetpassword')
    
    else:
        messages.error(request, 'This link has expired!')
        return redirect('/sign_in')



def resetpassword(request):
    if request.method == 'POST':
            password = request.POST['password']
            confirm_password = request.POST['confirm_password']

            if password == confirm_password:
                uid = request.session.get('uid')
                user = Account.objects.get(pk=uid)
                user.set_password(password)
                user.save()
                messages.success(request, 'Password reset successful')
                return redirect('/sign_in')

            else:
                messages.error(request, 'Password do not match')
                return redirect('/resetpassword')
    else:
        return render(request, 'trade/account/resetpassword.html')


@login_required(login_url = 'sign_in')
def plans(request):
    plans = Plan.objects.all()
    return render(request, 'dash/plans.html', {'plans':plans})
 