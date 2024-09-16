from django.db import models
from django.core.mail import send_mail
from django.conf import settings

class Contact(models.Model):
    full_name = models.CharField(max_length=200,null=True,blank=True)
    email = models.EmailField(max_length=200,null=True,blank=True)
    message = models.TextField(max_length=500,null=True,blank=True)

    class Meta:
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'

    def __str__(self):
        return str(self.full_name)
    
    # def save(self, *args, **kwargs):
    #     # Save the Contact object first
    #     super(Contact, self).save(*args, **kwargs)

    #     # Email content
    #     subject = 'New Contact Submission'
    #     message_body = (
    #         f'You have a new contact submission from {self.full_name}.\n\n'
    #         f'Message:\n{self.message}\n\n'
    #         f'Email: {self.email}'
    #     )

    #     recipient_list = [settings.ADMIN_EMAIL,]
    #     send_mail(
    #         subject=subject, 
    #         message=message_body, 
    #         from_email=settings.DEFAULT_FROM_EMAIL, 
    #         recipient_list=recipient_list
    #     )
       