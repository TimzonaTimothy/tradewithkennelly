from django.shortcuts import render,redirect, get_object_or_404
from django.urls import reverse_lazy,reverse
from django.contrib import messages
from accounts.models import *
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, JsonResponse,HttpResponse,HttpRequest
from .models import *
from django.contrib.auth import logout
from django.template import RequestContext
from django.conf import settings
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
    return render(request, 'new/index.html', {})

def faq(request):
    return render(request, 'new/faq.html', {})


def terms(request):
    return render(request, 'new/terms-and-conditions.html', {})

def privacy(request):
    return render(request, 'new/privacy-policy.html', {})

def plans(request):
    return render(request, 'new/plans.html', {})

def services(request):
    return render(request, 'new/services.html', {})

def glossary(request):
    return render(request, 'trade/glossary.html', {})

def market_data(request):
    return render(request, 'trade/market-data.html', {})

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
        return render(request, 'new/about-us.html', {})


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
        message_subject = request.POST['subject']
        message = request.POST['msg']

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
            subject = message_subject,
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
        return render(request, 'new/contact.html', context={})

def newsletter_sub(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        bot = request.POST.get('bot')
        if bot:
            return JsonResponse({'error': 'Bot detected'}, status=400)
        elif not email:
            return JsonResponse({'error': 'Email is required'}, status=400)
        elif Newsletter.objects.filter(email=email).exists():
            return JsonResponse({'error': 'Email already exists'}, status=400)
        else:
            newsletter = Newsletter(email=email)
            newsletter.save()
            return JsonResponse({'success': 'Email submitted successfully'})
