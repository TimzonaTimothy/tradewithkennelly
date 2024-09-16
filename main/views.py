from django.shortcuts import render,redirect, get_object_or_404
from django.urls import reverse_lazy,reverse
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from accounts.models import *
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .models import Contact
from django.contrib.auth import logout
from django.template import RequestContext
from django.conf import settings
from django.http import HttpRequest
from ipware import get_client_ip
from .utils import get_country_from_ip

def send_visitor_notification_email(ip_address, country):
    subject = 'New Visitor Alert'
    message = f'A new visitor from {country} (IP: {ip_address}) has visited your website.'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = ['arizonatymothy@gmail.com']
    
    send_mail(subject, message, from_email, recipient_list)

def home(request, *args, **kwargs):
    ref_code = request.GET.get('ref_code')
    if ref_code:
        request.session['ref_code'] = ref_code
        request.session.set_expiry(86400)
    
    # if not request.user.is_authenticated:
    #     if not request.session.get('email_sent', False):
    #         # Get the visitor's IP address
    #         client_ip, is_routable = get_client_ip(request)
    #         if client_ip is None:
    #             client_ip = '0.0.0.0'
            
    #         # Check if the IP address is not from localhost
    #         if client_ip not in ['127.0.0.1', '::1']:
    #             # Get the country from the IP address
    #             country = get_country_from_ip(client_ip)
                
    #             # Send email notification
    #             # send_visitor_notification_email(client_ip, country)
    #             print(client_ip, country)
                
    #             # Set the session flag to indicate email has been sent
    #             request.session['email_sent'] = True
    #             request.session.set_expiry(86400)
    
    if request.method == "POST":
        message_name = request.POST['name'] 
        message_email = request.POST['email']
        message = request.POST['message']
            
        try:
            bot = request.POST.get('bot-c')
            if bot == '':
                pass
            else:
                return redirect('/')
        except:
            pass

        Contact.objects.create(
            full_name=message_name,
            email=message_email,
            message=message
        )
        messages.success(request, 'Your email has been sent')
        return HttpResponseRedirect('home')
    return render(request, 'trade/index.html', {})

def faq(request):
    return render(request, 'trade/faq.html', {})

def glossary(request):
    return render(request, 'trade/glossary.html', {})

def market_data(request):
    return render(request, 'trade/market-data.html', {})

def terms(request):
    return render(request, 'trade/terms.html', {})

def privacy(request):
    return render(request, 'trade/privacy.html', {})

def plans(request):
    return render(request, 'trade/plans.html', {})

def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

def about(request):
    if request.method == "POST":
        message_name = request.POST['name'] 
        message_email = request.POST['email']
        message = request.POST['message']
            
        #send mai
        try:
            bot = request.POST.get('bot-c')
            if bot == '':
                pass
            else:
                return redirect('/about')
        except:
            pass

        Contact.objects.create(
            full_name=message_name,
            email=message_email,
            message=message
        )    
            
        send_mail(
            message_name + ' ' +' sent you an enquiry '+ 'Email '+ message_email + ' ',
            message,
            'arizonatymothy@gmail.com',
            ['arizonatymothy@gmail.com'],
            fail_silently=False
        )    
        messages.success(request, 'Your email has been sent')
        return HttpResponseRedirect('about')
    else:
        return render(request, 'trade/about.html', {})


def handler404(request, exception, template_name="404.html"):
    response = render(template_name)
    response.status_code = 404
    return response


def handler500(request, *args, **argv):
    response = render('500.html', {},
    context_instance=RequestContext(request))
    response.status_code = 500
    return response


def contact(request):
    if request.method == "POST":
        message_name = request.POST['name'] 
        message_email = request.POST['email']
        message = request.POST['message']

        try:
            bot = request.POST.get('bot-c')
            if bot == '':
                pass
            else:
                return redirect('/contact')
        except:
            pass

        Contact.objects.create(
            full_name=message_name,
            email=message_email,
            message=message
        )
            
        #send mai
        # send_mail(
        #     message_name + ' ' +' sent you an enquiry '+ 'Email '+ message_email + ' ',
        #     message,
        #     'arizonatymothy@gmail.com',
        #     ['arizonatymothy@gmail.com'],
        #     fail_silently=False
        # )       
        messages.success(request, 'Successfully sent!')
        return HttpResponseRedirect('contact')
    else:
        return render(request, 'trade/contact.html', context={})