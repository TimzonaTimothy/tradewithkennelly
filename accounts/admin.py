from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html

from django.utils.safestring import mark_safe
import threading
from django.conf import settings
from django.http import HttpResponse
from django.core.mail import (send_mail, BadHeaderError, EmailMessage)
from django.contrib.auth import get_user_model
User = get_user_model()

# Register your models here.

class AccountAdmin(UserAdmin):
    def thumbnail(self, object):
        return format_html('<img src="{}" width="30" style="border-raduis:50%;">'.format(object.profile_picture.url))
    thumbnail.short_description = 'Profile Picture'
    
    list_display = ('email', 'first_name', 'last_name', 'username', 'last_login', 'date_joined', 'is_active')
    list_display_links = ('email', 'first_name', 'last_name')
    readonly_fields = ('last_login', 'date_joined', 'recommended_by')
    ordering = ('-date_joined',)
    search_fields = ['username', 'email', 'first_name', 'last_name']
    filter_horizontal = ()
    list_filter = ()
    fieldsets = (
        ('Authenticators', {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'username', 'state', 'country', 'recommended_by', 'code')}),
        ('Balances', {'fields': ('balance','total_invest','total_withdrawn','total_earned','bitcoin_address')}),
        ('Checks', {'fields': ('date_joined', 'last_login', 'is_admin', 'is_staff', 'is_active', 'is_superadmin')}),
        # ('OTP', {'fields': ('otp','otp_created_at')}),
    )
    list_per_page = 25

class UserProfileAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        return format_html('<img src="{}" width="30" style="border-raduis:50%;">'.format(object.profile_picture.url))
    thumbnail.short_description = 'Profile Picture'
    list_display = ('thumbnail', 'user', 'city', 'state', 'country',)

admin.site.register(Account, AccountAdmin)

# admin.site.register(Wallet)
# admin.site.register(Plan)

class ReferralAdmin(admin.ModelAdmin):
    list_display = ('referrer', 'referred', 'created')
    list_display_links = ('referrer', 'referred', 'created')
    ordering = ('-created',)
    search_fields = ['referrer__username', 'referred__username']
    filter_horizontal = ()
    list_filter = ()
    fieldsets = (
        ('Authenticators', {'fields': ('referrer', 'referred')}),
    )
    list_per_page = 25


admin.site.register(Referral,ReferralAdmin)


admin.site.site_header = 'ADMIN'
admin.site.site_title = 'ADMINISTRATION'