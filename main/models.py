from django.db import models
from django.core.mail import send_mail
from django.conf import settings

class Contact(models.Model):
    full_name = models.CharField(max_length=200,null=True,blank=True)
    email = models.EmailField(max_length=200,null=True,blank=True)
    subject = models.CharField(max_length=200,null=True,blank=True)
    message = models.TextField(max_length=500,null=True,blank=True)

    class Meta:
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'

    def __str__(self):
        return str(self.full_name)
           

class Newsletter(models.Model):
    email = models.EmailField(blank=True, null=True,unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.email)