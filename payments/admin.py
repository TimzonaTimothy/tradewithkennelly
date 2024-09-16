from django.contrib import admin
from .models import *
# Register your models here.

# admin.site.register(Referral_Withdrawal_Request)


from django.contrib import admin

class DepositCryptoAdmin(admin.ModelAdmin):

    fieldsets = (
        (None, {
            'fields': ('user', 'transaction_id', 'amount', 'Wallet_Type', 'detail', 'status', 'created_at', 'added_to_balance')
        }),
    )

    list_display = ['user', 'transaction_id','amount', 'status']
    list_filter = ['status', 'user']
    list_display_links = ['user', 'transaction_id','amount']
    search_fields = ['user__username', 'user__email', 'transaction_id']
    list_per_page = 20


class InvestmentCryptoAdmin(admin.ModelAdmin):
    

    fieldsets = (
        (None, {
            'fields': ('user', 'transaction_id', 'amount', 'Wallet_Type', 'percent', 'detail','status', 'created_at', 'added_to_balance')
        }),
    )

    list_display = ['user', 'transaction_id', 'amount', 'status']
    list_filter = ['status', 'user']
    list_display_links = ['user', 'transaction_id', 'amount']
    search_fields = ['user__username', 'user__email', 'transaction_id']
    list_per_page = 20


class TransactionAdmin(admin.ModelAdmin):
    

    fieldsets = (
        (None, {
            'fields': ('user', 'transaction_id', 'amount','transaction_type', 'Wallet_Type','detail','created_at')
        }),
    )

    list_display = ['user', 'transaction_id', 'amount','transaction_type','Wallet_Type']
    list_filter = [ 'user']
    list_display_links = ['user', 'transaction_id', 'amount']
    search_fields = ['user', 'transaction_id']
    list_per_page = 20

# admin.site.register(Deposit, DepositCryptoAdmin)
admin.site.register(Investment, InvestmentCryptoAdmin)
admin.site.register(Transaction, TransactionAdmin)

# class OrderAdmin(admin.ModelAdmin):
#     list_display = ['user','transaction_id','plan','amount','status','investment_type',]
#     list_filter = ['status', 'user',]
#     list_display_links = ('transaction_id','plan','amount')
#     search_fields = ['transaction_id','btc_hash_code','plan',]
#     list_per_page = 20
    

# admin.site.register(Crypto,OrderAdmin)


class WithrawalAdmin(admin.ModelAdmin):
    list_display = ['user','amount','crypto','status',]
    list_filter = ['status',]
    list_display_links = ('user','amount','crypto','status')
    search_fields = ['user','amount','crypto',]
    list_per_page = 20
    
admin.site.register(Crypto_Withdrawal_Request, WithrawalAdmin)

