from django.conf import settings
from .models import *
from django.db.models.signals import post_save
from django.dispatch import receiver
import secrets
from django.contrib.auth import get_user_model

User = get_user_model()

def get_random_string(user,length=3, allowed_chars= '0123456789'):
    code = ''.join(secrets.choice(allowed_chars) for i in range(length))
    main_code = code + user.username
    if User.objects.filter(code=main_code).exists():
        main_code = get_random_string(user)
    return str(main_code)

def generate_ref_code(sender, instance, created, **kwargs):
    if created:
        instance.code = get_random_string(instance)
        instance.save()

post_save.connect(generate_ref_code, sender=User)