import pyotp
from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
import geocoder

def get_country_from_ip(ip_address):
    response = geocoder.ipinfo(ip_address)
    if response.ok:
        return response.country
    return 'Unknown'

def get_client_ip(request):
    """Get client IP address from request headers."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


User = get_user_model()

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