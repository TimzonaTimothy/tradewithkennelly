from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,PermissionsMixin
from django.utils.crypto import get_random_string
            
class MyAccountManager(BaseUserManager):
    def create_user(self,email, first_name,last_name,username,password=None):
        if not email:
            raise ValueError('User must have an email address')

        if not username:
            raise ValueError('User must have username')

        user = self.model(
            email = self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name = last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email,username,password):
        user = self.create_user(
            email = self.normalize_email(email),
            username=username,
            password=password,
        )

        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser,PermissionsMixin):
    first_name    = models.CharField(max_length=100,blank=True, null=True)
    last_name     = models.CharField(max_length=100,blank=True, null=True)
    username     = models.CharField(max_length=100, unique=True)
    email         = models.EmailField(max_length=100, unique=True)
    bitcoin_address = models.CharField(blank=True, max_length=200)
    balance = models.DecimalField(max_digits=20,default=0.00,decimal_places=2,blank=True, null=True)
    total_invest = models.DecimalField(max_digits=20,default=0.00,decimal_places=2,blank=True, null=True)
    total_withdrawn = models.DecimalField(max_digits=20,default=0.00,decimal_places=2,blank=True, null=True)
    total_earned = models.DecimalField(max_digits=20,default=0.00,decimal_places=2,blank=True, null=True)
    state = models.CharField(blank=True,null=True, max_length=100) 
    country = models.CharField(blank=True, max_length=100) 
    code = models.CharField(max_length=100, verbose_name="Referral code",unique=True, null=True)
    recommended_by = models.CharField(blank=True, null=True, max_length=300)

    otp = models.CharField(max_length=6, blank=True, null=True)
    otp_created_at = models.DateTimeField(blank=True, null=True)

    date_joined   = models.DateTimeField(auto_now_add=True) 
    last_login    = models.DateTimeField(auto_now_add=True)   
    is_admin      = models.BooleanField(default=False)
    is_staff      = models.BooleanField(default=False)
    is_active     = models.BooleanField(default=True)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]

    objects = MyAccountManager()


    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return str(self.username)

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_superuser

    def has_module_perms(self, add_label):
        return True

    @property
    def total_referrals(self):
        if not hasattr(self, "referrals"):
            return None
        return self.referrals.all()

    @property
    def total_referrals_count(self):
        if self.total_referrals == None:
            return 0
        return self.referrals.all().count()

    @property
    def recommended_by(self):
        if not hasattr(self, 'referral'):
            return None
        return self.referral.referrer.username

    # @property
    # def referral_balance(self):
    #     if self.total_referrals == None:
    #         return 0
    #     return int(int(self.total_referrals.filter(withdrawn=False).count()) *0)
    
class Referral(models.Model):
    referrer = models.ForeignKey(Account, related_name="referrals",on_delete=models.CASCADE, null=True)
    referred = models.OneToOneField(Account, on_delete=models.CASCADE, null=True)
    withdrawn = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)

    def  __str__(self):
        return f"Referrer: {self.referrer.username} || Referred: {self.referred.username}"


from django.contrib.auth import get_user_model
User = get_user_model()


class Wallet(models.Model):
    wallet_type = models.CharField(max_length=500, blank=False, null=True)
    wallet_address = models.CharField(max_length=500, blank=False, null=True)
    # qr_code = models.ImageField(blank=True, upload_to='userprofile')

    class Meta:
        verbose_name = 'Wallet'
        verbose_name_plural = 'Wallets'

    def __str__(self):
        return self.wallet_type
        

class Plan(models.Model):
    plan_name = models.CharField(max_length=500, blank=False, null=True)
    minimum_amount = models.DecimalField(max_digits=20,decimal_places=2,blank=True, null=True)
    maximum_amount = models.DecimalField(max_digits=20,decimal_places=2,blank=True, null=True)
    duration_in_hours = models.IntegerField(blank=False, null=True)
    roi = models.IntegerField(blank=False, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name = 'Plan'
        verbose_name_plural = 'Plans'
        ordering=['created',]

    def __str__(self):
        return self.plan_name
    
        