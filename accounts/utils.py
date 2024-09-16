
import pyotp
import random
from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

User = get_user_model()

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp_via_email(email, otp):
    message = f'Your OTP code is {otp}. It is valid for 10 minutes.'
    mail_subject = 'OTP Code'
    message = render_to_string('crypto/auth/otp-mail.html', {
        'message':message,
        'otp':otp,
        })
    to_email = email
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email.content_subtype = "html"
    send_email.send()
    print(f"Your OTP is {otp}")

def send_otp(request, email):
    totp = pyotp.TOTP(pyotp.random_base32(), interval=480)
    otp = totp.now()
    request.session['otp_secret_key'] = totp.secret
    valid_date = datetime.now() + timedelta(minutes=30)
    request.session['otp_valid_date'] = str(valid_date)
    user = get_object_or_404(User, email=email)
    mail_subject = 'OTP Code'
    message = render_to_string('user/otp-mail.html', {
        'user':user,
        'otp':otp,
        })
    to_email = user.email
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email.content_subtype = "html"
    send_email.send()



    print(f"Your OTP is {otp}")