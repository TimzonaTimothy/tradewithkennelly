from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('transfer', views.transfer, name="transfer"),
    path('crypto-deposit/', views.deposit, name='deposit'),
    path('confirm_deposit', views.confirm_deposit, name="confirm_deposit"),
    path('deposit_histroy',views.deposit_histroy, name="deposit_histroy"),
    path('invest',views.invest, name="invest"),
    path('investments', views.investments, name='investments'),
    path('investments_histroy',views.investments_histroy, name="investments_histroy"),
    path('withdraw', views.withdraw, name='withdraw'),
    path('withdraw_histroy', views.withdraw_histroy, name="withdraw_histroy"),
    path('transactions',views.transactions,name="transactions"),
    path('order_detail/<str:order_id>/', views.order_detail, name='order_detail'),
]