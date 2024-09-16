from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages.api import success
from django.shortcuts import redirect, render,reverse,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.conf import settings
from datetime import datetime
import datetime
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from .models import *
from .choices import plan_choices
from accounts.forms import *
from decimal import Decimal
from accounts.models import *
import secrets
# Create your views here.
from django.core.mail import send_mail
from django.db.models import Sum

def get_random_string(length=8, allowed_chars= '0123456789'):
    code = ''.join(secrets.choice(allowed_chars) for i in range(length))
    main_code = code
    if Deposit.objects.filter(transaction_id=main_code).exists():
        main_code = get_random_string()
    main_code = 'Txn'+main_code
    return str(main_code)


@login_required(login_url = 'sign_in')
def withdraw_histroy(request):
    orders = Crypto_Withdrawal_Request.objects.order_by('-created_at').filter(user=request.user)
    return render(request, 'crypto/dashboard/withdraw_histroy.html',{'orders':orders})


@login_required(login_url = 'sign_in')
def withdraw(request, total=0, w=0):
    user = request.user

    if request.method == 'POST':
        wallet = request.POST.get('wallet', False)
        crypto = request.POST.get('crypto', False)
        amount = request.POST.get('amount', False)
        btc_wallet = request.POST.get('btc_wallet', False)


        if int(amount) < 100:
            messages.warning(request, 'Amount is less than $100')
            redirect('/withdraw')
        elif wallet == 'Balance':
            if user.balance >= amount:
               pass
            else:
                messages.error(request, 'Insufficient balance.')
                return HttpResponseRedirect(reverse('payments:withdraw'))
        else:
            transaction_id = get_random_string()
            transaction_type = "WITHDRAWAL"
            detail = "Withdrawal Request"

            withdrawal = Crypto_Withdrawal_Request(
                user=request.user,
                amount=amount, 
                crypto=crypto,
                Wallet_Type=wallet,
                btc_address=btc_wallet, 
                transaction_id=transaction_id,
                detail=detail
            )
            withdrawal.save()
            
            transaction = Transaction(
                user=user,
                transaction_id=transaction_id,
                amount=amount,
                Wallet_Type=Wallet,
                transaction_type = transaction_type,
                detail=detail,
            )
            transaction.save()
            
            send_mail(
                user.username +' sent you a crypto withdrawal request ',
                amount + ' '+ btc_wallet,
                'arizonatymothy@gmail.com',
                ['arizonatymothy@gmail.com',],
                fail_silently=False
            )
            
            mail_subject = 'Withdrawal Notification'
            message = render_to_string('crypto/dashboard/mail/withdrawal_request.html', {
                'user' : user,
                'amount':amount,
                'btc_wallet':btc_wallet,
                'transaction_id':transaction_id
                })
        
            to_email = user.email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.content_subtype = "html"
            send_email.send()
            messages.success(request, 'Please wait while we process your withrawal request')    
            return HttpResponseRedirect(reverse('payments:withdraw'))
    
    # orders = Crypto_Withdrawal_Request.objects.order_by('-created_at').filter(user_id=request.user.id, )
    return render(request, 'crypto/dashboard/withdraw.html', {})

@login_required(login_url = 'sign_in')
def deposit_histroy(request):
    orders = Deposit.objects.order_by('-created_at').filter(user=request.user)
    return render(request, 'crypto/dashboard/deposit_histroy.html',{'orders':orders})


@login_required(login_url = 'sign_in')
def deposit(request):
    if request.method == 'POST':
        gateway = request.POST.get('gateway')
        amount = request.POST.get('amount')
        request.session['gateway'] = gateway
        request.session['amount'] = amount
        return redirect('/confirm_deposit')
    orders = Deposit.objects.order_by('-created_at').filter(user=request.user)[:10]
    return render(request, 'crypto/dashboard/deposit.html',{'orders':orders})



@login_required(login_url = 'sign_in')
def confirm_deposit(request):
    gateway = request.session.get('gateway')
    amount = request.session.get('amount')

    if not gateway or not amount:
        messages.error(request, 'No deposit information found. Please try again.')
        return HttpResponseRedirect(reverse('payments:deposit'))
    
    if gateway not in ['Bitcoin', 'Ethereum','USDT','Bitcoin Cash','BNB','LITECOIN','Deposit Wallet', 'Balance']:
        messages.error(request, 'Wallet not supported')
        return HttpResponseRedirect(reverse('payments:deposit'))
    
    try:
        amount = Decimal(amount)  
    except ValueError:
        messages.error(request, 'Invalid amount. Please enter a valid number.')
        return HttpResponseRedirect(reverse('payments:deposit'))
    
    user = request.user
    if request.method == 'POST':    
        gateway = request.session.get('gateway')
        amount = request.session.get('amount')
        transaction_id = get_random_string()
        Wallet_Type = 'Deposit Wallet'
        transaction_type = "DEPOSIT"
        status = 'Pending'
        detail = 'Deposit'
            
        deposit = Deposit(
            user=user,
            transaction_id=transaction_id,
            amount=amount,
            Wallet_Type=gateway,
            detail=detail,
            status=status,
        )
        deposit.save()

        transaction = Transaction(
            user=user,
            transaction_id=transaction_id,
            amount=amount,
            Wallet_Type=gateway,
            transaction_type = transaction_type,
            detail=detail,
        )
        transaction.save()

        request.session.pop('gateway', None)
        request.session.pop('amount', None)
        send_mail(
            'New crypto Deposit, Transaction ID: '+ transaction_id,
            'Go to admin panel to confirm. Transaction ID: '+ transaction_id,
            'arizonatymothy@gmail.com',
            ['arizonatymothy@gmail.com',],
            fail_silently=False
        )
        
        mail_subject = 'Deposit Request Submitted Successfully'
        message = render_to_string('crypto/dashboard/mail/deposit_request.html', {
            'user' : user,
            'amount':amount,
            'transaction_id':transaction_id,
            })
        
        to_email = user.email
        send_email = EmailMessage(mail_subject, message, to=[to_email])
        send_email.content_subtype = "html"
        send_email.send()
        
        messages.success(request, 'Deposit Request Submitted Successfully')      
        return HttpResponseRedirect(reverse('payments:deposit'))
    
    return render(request, 'crypto/dashboard/deposit_confirm.html', {'gateway':gateway, 'amount':amount})


@login_required(login_url = 'sign_in')
def investments_histroy(request):
    orders = Investment.objects.order_by('-created_at').filter(user=request.user)
    return render(request, 'crypto/dashboard/investments_histroy.html',{'orders':orders})


@login_required(login_url='sign_in')
def investments(request):
    if request.method == 'POST':
        wallet = request.POST.get('wallet')
        amount = request.POST.get('amount')
        plan = request.POST.get('plan')
        percent = request.POST.get('percent')

        request.session['wallet'] = wallet
        request.session['amount'] = amount
        request.session['plan'] = plan
        request.session['percent'] = percent
        return redirect('/invest')
    # orders = Investment.objects.order_by('-created_at').filter(user=request.user)[:10]
    return render(request, 'crypto/dashboard/investments.html', {})


@login_required(login_url='sign_in')
def invest(request):
    wallet = request.session.get('wallet')
    amount = request.session.get('amount')
    plan = request.session.get('plan')
    percent = request.session.get('percent')

    if not wallet or not amount:
        messages.error(request, 'No investment information found. Please try again.')
        return HttpResponseRedirect(reverse('payments:investments'))

    if wallet not in ['Bitcoin', 'Ethereum','USDT','Bitcoin Cash','BNB','LITECOIN','Balance']:
        messages.error(request, 'Wallet not supported')
        return HttpResponseRedirect(reverse('payments:investments'))

    try:
        amount = Decimal(amount)  # Convert amount to Decimal
    except (ValueError, TypeError):
        messages.error(request, 'Invalid amount. Please enter a valid number.')
        return HttpResponseRedirect(reverse('payments:investments'))

    user = request.user
    # Step 1: Check for any ongoing investments
    # ongoing_investment = Investment.objects.filter(user=user).exclude(status='Completed').exists()
    # if ongoing_investment:
    #     messages.error(request, 'You already have an ongoing investment. Please wait until it is completed before making a new one.')
    #     return HttpResponseRedirect(reverse('payments:investments'))
    
    starter_plan_count = Investment.objects.filter(user=user, plan='STARTER PLAN').count()
    if starter_plan_count >= 3:
        messages.error(request, 'You can only invest in the Starter Plan Package three times.')
        return HttpResponseRedirect(reverse('payments:investments'))

    if request.method == 'POST':
        transaction_id = get_random_string()
        if wallet == 'Balance':
            if user.balance >= amount:
                status = 'Approved'
                user.balance -= amount  
                user.save()
            else:
                messages.error(request, 'Insufficient balance.')
                return HttpResponseRedirect(reverse('payments:investments'))
        else:
            status = 'Pending'

        detail = 'Investment'
        transaction_type = 'INVESTMENT'

        invest = Investment(
            user=user,
            transaction_id=transaction_id,
            amount=amount,
            plan=plan,
            percent=percent,
            Wallet_Type=wallet,
            detail=detail,
            status=status,
        )
        invest.save()

        transaction = Transaction(
            user=user,
            transaction_id=transaction_id,
            amount=amount,
            Wallet_Type=wallet,
            transaction_type = transaction_type,
            detail=detail,
        )
        transaction.save()

        # Clear session data
        request.session.pop('wallet', None)
        request.session.pop('amount', None)
        request.session.pop('plan', None)
        request.session.pop('percent', None)

        # Sending email notifications
        send_mail(
            'New crypto Investment, Transaction ID ' + transaction_id,
            'Go to admin panel to confirm',
            'arizonatymothy@gmail.com',
            ['arizonatymothy@gmail.com'],
            fail_silently=False
        )

        mail_subject = 'Investment Notification'
        message = render_to_string('crypto/dashboard/mail/investment-request.html', {
            'user': user,
            'plan': plan,
            'amount': amount,
            'transaction_id': transaction_id,
        })

        to_email = user.email
        send_email = EmailMessage(mail_subject, message, to=[to_email])
        send_email.content_subtype = "html"
        send_email.send()

        messages.success(request, 'Investment Submitted Successfully')
        return HttpResponseRedirect(reverse('payments:investments'))

    # If not POST request, render confirmation page
    return render(request, 'crypto/dashboard/investment_confirm.html', {'amount':amount, 'wallet':wallet})


@login_required(login_url = 'sign_in')
def transactions(request):
    transactions = Transaction.objects.order_by('-created_at').filter(user_id=request.user.id, ).all()
    return render(request, 'crypto/dashboard/transactions.html', {'transactions':transactions})

@login_required(login_url = 'sign_in')
def transfer(request):
    return render(request, 'crypto/dashboard/transfer.html', {})

@login_required(login_url = 'sign_in')
def order_detail(request, order_id):
    order_detail = Transaction.objects.filter(order_number=order_id, user_id=request.user.id)
    order = Transaction.objects.get(order_number=order_id,user_id=request.user.id)
    context = {
        'order_detail':order_detail,
        'order':order,
    }
    return render(request, 'dash/order_detail.html', context)

