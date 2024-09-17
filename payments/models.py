from django.db import models
from accounts.models import Account
from datetime import datetime
from django.utils import timezone
from django.db.models.deletion import SET_NULL
# Create your models here.
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.db.models.signals import post_save
from django.dispatch import receiver
from decimal import Decimal

class Crypto_Withdrawal_Request(models.Model):
    STATUS = (
        ('Pending','Pending'),
        ('Paid','Paid'),
        ('Cancelled', 'Cancelled'),
    )
    user = models.ForeignKey(Account, on_delete=models.CASCADE,  null=True)
    amount = models.DecimalField(max_digits=20,decimal_places=2,blank=True, null=True)
    crypto = models.CharField(max_length=300, blank=True, null=True)
    Wallet_Type = models.CharField(max_length=500, blank=True, null=True)
    detail = models.CharField(max_length=500, blank=True, null=True)
    btc_address = models.CharField(max_length=5000,blank=True, null=True)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    transaction_hash = models.CharField(max_length=5000,blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS, default='Pending',null=True)
    remove_from_balance = models.BooleanField(default=False,null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name = 'Withdrawal'
        verbose_name_plural = 'Withdrawals'
    
    def save(self):
        if self.id:
            old = Crypto_Withdrawal_Request.objects.get(pk=self.id)
            if old.status == 'Pending' and self.status == 'Paid':
                if self.Wallet_Type == 'Balance':
                    self.user.balance -= self.amount
                    self.user.total_withdrawn += self.amount
                    self.user.save()
                self.remove_from_balance = True
                amount = self.amount
                user = self.user
                btc_address = self.btc_address
                transaction_id = self.transaction_id
                
                mail_subject = 'Crypto Payment Notification'
                message = render_to_string('crypto/dashboard/mail/withdrawal_complete.html', {
                    'user' : user,
                    'amount':amount,
                    'btc_address':btc_address,
                    'transaction_id':transaction_id,
                    })
            
                to_email = user.email
                send_email = EmailMessage(mail_subject, message, to=[to_email])
                send_email.content_subtype = "html"
                send_email.send()
            if old.status == 'Pending' and self.status == 'Cancelled':
                self.send_notification('crypto/dashboard/mail/withdrawal-cancel.html', 'Investment cancelled')
        super(Crypto_Withdrawal_Request, self).save()

    def send_notification(self, template, subject):
        message = render_to_string(template, {
            'user' : self.user,
            'amount':self.amount,
            'btc_address':self.btc_address,
            'transaction_id':self.transaction_id,
        })
        to_email = self.user.email
        send_email = EmailMessage(subject, message, to=[to_email])
        send_email.content_subtype = "html"
        send_email.send()

class Deposit(models.Model):
    STATUS = (
        ('Pending','Pending'),
        ('Approved', 'Approved'),
        ('Cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    plan = models.CharField(max_length=500, blank=True, null=True)
    amount = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    Wallet_Type = models.CharField(max_length=500, blank=True, null=True)
    detail = models.CharField(max_length=500, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS, default='Pending', null=True)
    created_at = models.DateTimeField(default=timezone.now, blank=True, null=True)
    added_to_balance = models.BooleanField(default=False, null=True)

    def __str__(self):
        return self.transaction_id

    class Meta:
        verbose_name = 'Deposit'
        verbose_name_plural = 'Deposits'

    def save(self, *args, **kwargs):
        if self.id:
            old = Deposit.objects.get(pk=self.id)

            if old.status == 'Pending' and self.status == 'Approved':
                self.user.crypto_balance += self.amount
                self.added_to_balance = True
                self.user.save()
                self.send_notification('crypto/dashboard/mail/deposit-approve.html', 'Deposit Request Approved')

            # if old.status == 'Approved' and self.status == 'Completed':
            #     self.send_notification('crypto/dashboard/mail/deposit-complete.html', 'Investment Completed')
            
            if old.status == 'Pending' and self.status == 'Cancelled':
                self.send_notification('crypto/dashboard/mail/deposit-cancel.html', 'Investment cancelled')

        super(Deposit, self).save(*args, **kwargs)

    def send_notification(self, template, subject):
        message = render_to_string(template, {
            'user': self.user,
            'detail':self.detail,
            'amount': self.amount,
            'transaction_id': self.transaction_id,
            'plan': self.plan,
        })
        to_email = self.user.email
        send_email = EmailMessage(subject, message, to=[to_email])
        send_email.content_subtype = "html"
        send_email.send()


class Investment(models.Model):
    STATUS = (
        ('Pending','Pending'),
        ('Approved', 'Approved'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    plan = models.CharField(max_length=500, blank=True, null=True)
    amount = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    Wallet_Type = models.CharField(max_length=500, blank=True, null=True)
    detail = models.CharField(max_length=500, blank=True, null=True)
    percent = models.DecimalField(max_digits=20,default=0.00,decimal_places=2,blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS, default='Pending', null=True)
    created_at = models.DateTimeField(default=timezone.now, blank=True, null=True)
    added_to_balance = models.BooleanField(default=False, null=True)

    CHILD_COMMISSION_PERCENTAGE = 10  # 10% for the child
    PARENT_COMMISSION_PERCENTAGE = 5  # 5% for the parent

    def __str__(self):
        return self.transaction_id

    @property    
    def percentage(self):
        # Convert amount and percent to Decimal
        amount = Decimal(self.amount or 0)
        percent = Decimal(self.percent or 0)
        return (amount * percent / Decimal('100')) + amount
    
    class Meta:
        verbose_name = 'Investment'
        verbose_name_plural = 'Investments'

    def save(self, *args, **kwargs):
        if self.id:
            old = Investment.objects.get(pk=self.id)
            if old.status == 'Pending' and self.status == 'Approved':
                self.user.balance += self.amount
                self.added_to_balance = True
                self.user.save()
                self.add_commission()
                self.send_notification('crypto/dashboard/mail/investment-approve.html', 'Investment Request Approved')

            if old.status == 'Approved' and self.status == 'Completed':
                self.send_notification('crypto/dashboard/mail/investment-complete.html', 'Investment Completed')
            
            if old.status == 'Pending' and self.status == 'Cancelled':
                self.send_notification('crypto/dashboard/mail/investment-cancel.html', 'Investment cancelled')

        super(Investment, self).save(*args, **kwargs)

    def send_notification(self, template, subject):
        message = render_to_string(template, {
            'user': self.user,
            'detail':self.detail,
            'amount': self.amount,
            'transaction_id': self.transaction_id,
            'plan': self.plan,
        })
        to_email = self.user.email
        send_email = EmailMessage(subject, message, to=[to_email])
        send_email.content_subtype = "html"
        send_email.send()
    
    def add_commission(self):
        """Add commission to both the referrer and the grand-referrer."""
        if self.user.recommended_by:
            # Child (current user) earns 10%
            referrer = Account.objects.get(username=self.user.recommended_by)
            child_commission = self.amount * (self.CHILD_COMMISSION_PERCENTAGE / 100)
            referrer.balance += child_commission
            referrer.save()
            self.send_commission_notification(self.amount, referrer, child_commission, "child")

            # Parent (referrer's referrer) earns 5%
            if referrer.recommended_by:
                parent_referrer = Account.objects.get(username=referrer.recommended_by)
                parent_commission = self.amount * (self.PARENT_COMMISSION_PERCENTAGE / 100)
                parent_referrer.balance += parent_commission
                parent_referrer.save()
                self.send_commission_notification(self.amount, parent_referrer, parent_commission, "parent")

    def send_commission_notification(self, amount,referrer, commission, role):
        message = render_to_string('crypto/dashboard/mail/commission_notification.html', {
            'amount':amount,
            'referrer': referrer.full_name(),
            'commission': commission,
             'role': role
        })
        to_email = referrer.email
        send_email = EmailMessage('Commission Earned', message, to=[to_email])
        send_email.content_subtype = "html"
        send_email.send()

class Transaction(models.Model):
    TRANSACTION_CHOICES = [
        ('DEPOSIT', 'Deposit'),
        ('INVESTMENT', 'Investment'),
        ('WITHDRAWAL', 'Withdrawal'),
    ]
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    transaction_type = models.CharField(max_length=50, choices=TRANSACTION_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    Wallet_Type = models.CharField(max_length=500, blank=True, null=True)
    detail = models.CharField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now, blank=True, null=True)

    def __str__(self):
        return f'{self.transaction_type} of {self.amount} on {self.created_at}'
    
    class Meta:
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'
    
# class Crypto(models.Model):
#     STATUS = (
#         ('Pending','Pending'),
#         ('Approved', 'Approved'),
#         ('Completed', 'Completed'),
#         ('Cancelled', 'Cancelled'),
#     )

#     CHOICE = (
#         ('Deposit','Deposit'),
#         ('Investment','Investment'),
#     )

#     user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
#     transaction_id = models.CharField(max_length=100, blank=True, null=True)
#     plan = models.CharField(max_length=500, blank=True, null=True)
#     amount = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
#     Wallet_Type = models.CharField(max_length=500, blank=True, null=True)
#     detail = models.CharField(max_length=500, blank=True, null=True)
#     investment_type = models.CharField(max_length=500, choices=CHOICE, blank=True, null=True)
#     percent = models.IntegerField(blank=True, null=True)
#     status = models.CharField(max_length=20, choices=STATUS, default='Pending', null=True)
#     created_at = models.DateTimeField(default=timezone.now, blank=True, null=True)
#     added_to_balance = models.BooleanField(default=False, null=True)

#     def __str__(self):
#         return self.transaction_id

#     @property    
#     def percentage(self):
#         # Convert amount and percent to Decimal
#         amount = Decimal(self.amount or 0)
#         percent = Decimal(self.percent or 0)
#         return (amount * percent / Decimal('100')) + amount
    
#     class Meta:
#         verbose_name = 'Investment'
#         verbose_name_plural = 'Investments'

#     def save(self, *args, **kwargs):
#         if self.id:
#             old = Crypto.objects.get(pk=self.id)

#             if old.investment_type == 'Deposit' and old.status == 'Pending' and self.status == 'Approved':
#                 self.user.crypto_balance += self.amount
#                 self.added_to_balance = True
#                 self.user.save()
#                 self.send_notification('crypto/dashboard/mail/deposit-approve.html', 'Deposit Request Approved')

#             # if old.investment_type == 'Investment':
#             #     self.user.crypto_balance -= self.amount
#             #     percent = self.amount * (self.percent / 100)
#             #     self.user.interest_wallet += percent
#             #     self.user.save()
#             #     self.send_notification('crypto/dashboard/mail/deposit-approve.html', 'Investment Request Approved')

#             if old.status == 'Approved' and self.status == 'Completed':
#                 self.send_notification('crypto/dashboard/mail/deposit-complete.html', 'Investment Completed')
            
#             if old.status == 'Pending' and self.status == 'Cancelled':
#                 self.send_notification('crypto/dashboard/mail/deposit-cancel.html', 'Investment cancelled')

#         super(Crypto, self).save(*args, **kwargs)

#     def send_notification(self, template, subject):
#         message = render_to_string(template, {
#             'user': self.user,
#             'detail':self.detail,
#             'amount': self.amount,
#             'transaction_id': self.transaction_id,
#             'plan': self.plan,
#         })
#         to_email = self.user.email
#         send_email = EmailMessage(subject, message, to=[to_email])
#         send_email.content_subtype = "html"
#         send_email.send()

# class Deposit(Crypto):
#     class Meta:
#         proxy = True
#         verbose_name = 'Deposit'
#         verbose_name_plural = 'Deposits'

# class Investment(Crypto):
#     class Meta:
#         proxy = True
#         verbose_name = 'Investment'
#         verbose_name_plural = 'Investments'



# class Crypto(models.Model):
#     STATUS = (
#         ('NEW', 'NEW'),
#         ('Accepted', 'Accepted'),
#         ('Completed', 'Completed'),
#         ('Cancelled', 'Cancelled'),
#     )

#     user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
#     transaction_id = models.CharField(max_length=100, blank=True, null=True)
#     plan = models.CharField(max_length=500, blank=True, null=True)
#     amount = models.IntegerField(blank=True, default=0, null=True)
#     investment_type = models.CharField(max_length=500, blank=True, null=True)
#     btc_address = models.CharField(max_length=1000, blank=True, null=True)
#     btc_hash_code = models.CharField(max_length=1000, blank=True, null=True)
#     status = models.CharField(max_length=20, choices=STATUS, default='NEW', null=True)
#     created_at = models.DateTimeField(default=timezone.now, blank=True, null=True)
#     is_ordered = models.BooleanField(default=False)
#     added_to_balance = models.BooleanField(default=False, null=True)

#     COMMISSION_PERCENTAGE = 10  # commission percentage

#     def __str__(self):
#         return self.transaction_id

#     class Meta:
#         verbose_name = 'Investment'
#         verbose_name_plural = 'Investments'

#     def save(self, *args, **kwargs):
#         if self.id:
#             old = Crypto.objects.get(pk=self.id)
#             if old.status == 'NEW' and self.status == 'Accepted':
#                 self.user.crypto_balance += self.amount
#                 self.user.save()
#                 self.add_commission()
#                 self.send_notification('dash/crypto-approval.html', 'Investment Notification')
#             if old.status == 'Accepted' and self.status == 'Completed':
#                 self.send_notification('dash/crypto-confirm.html', 'Investment Notification')
#         super(Crypto, self).save(*args, **kwargs)

#     def add_commission(self):
#         if self.user.recommended_by:
#             referrer = Account.objects.get(username=self.user.recommended_by)
#             commission = self.amount * (self.COMMISSION_PERCENTAGE / 100)
#             referrer.crypto_balance += commission
#             amount = self.amount
#             referrer.save()
#             self.send_commission_notification(amount,referrer, commission)

#     def send_notification(self, template, subject):
#         message = render_to_string(template, {
#             'user': self.user,
#             'amount': self.amount,
#             'transaction_id': self.transaction_id,
#             'plan': self.plan,
#         })
#         to_email = self.user.email
#         send_email = EmailMessage(subject, message, to=[to_email])
#         send_email.content_subtype = "html"
#         send_email.send()

#     def send_commission_notification(self, amount,referrer, commission):
#         message = render_to_string('dash/commission_notification.html', {
#             'amount':amount,
#             'referrer': referrer.full_name(),
#             'commission': commission,
#         })
#         to_email = referrer.email
#         send_email = EmailMessage('Commission Earned', message, to=[to_email])
#         send_email.content_subtype = "html"
#         send_email.send()



# class Bonus(models.Model):
#     STATUS = (
#         ('Added','Added'),
#         ('Pending', 'Pending'),
#     )
#     user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
#     amount = models.IntegerField(default='0', null=True)
#     comment = models.CharField(max_length=500,blank=True,null=True)
#     status = models.CharField(max_length=20, choices=STATUS, default='Added',null=True)
#     created_at = models.DateTimeField(default=timezone.datetime.now,blank = True, null=True)
#     added_to_balance = models.BooleanField(default=False, null=True)

#     def __str__(self):
#         return f"{self.user} {self.amount}"
        
#     class Meta:
#         verbose_name = 'Bonus'
#         verbose_name_plural = 'Bonuses'

#     def save(self, *args, **kwargs):
#         if self.id:
#             old = Bonus.objects.get(pk=self.id)
#             if old.status == 'Pending' and self.status == 'Added':
#                 self.user.crypto_balance += self.amount
#                 self.user.save()
#                 self.added_to_balance = True
#                 self.send_notification()
#         else:
#             if self.status == 'Added' and not self.added_to_balance:
#                 self.user.crypto_balance += self.amount
#                 self.user.save()
#                 self.added_to_balance = True
#                 self.send_notification()

#         super(Bonus, self).save(*args, **kwargs)

#     def send_notification(self):
#         user = self.user
#         amount = self.amount
#         comment = self.comment
#         current_site = 'https://blessedseedinvestltd.com/'
#         mail_subject = 'Bonus Notification'
#         message = render_to_string('dash/bonus.html', {
#             'user': user,
#             'amount': amount,
#             'comment': comment,
#             'domain': current_site,
#         })

#         to_email = user.email
#         send_email = EmailMessage(mail_subject, message, to=[to_email])
#         send_email.content_subtype = "html"
#         send_email.send()