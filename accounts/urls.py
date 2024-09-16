from django.urls import path, re_path, reverse_lazy
from .views import *
from django.conf import settings
from django.conf.urls.static import static
# from django.conf.urls import url 

from . import views



app_name = 'accounts'

urlpatterns = [
    path('sign_up', sign_up, name='sign_up'),
    # path('otp', otp_view, name='otp'),
    path('sign_in', sign_in, name='sign_in'),
    path('logout', user_logout, name='logout'),
    path('validate_earning',validate_earning,name="validate_earning"),
    path('dashboard', dashboard, name='dashboard'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('change_password', change_password, name='change_password'),
    path('edit_profile', edit_profile, name='edit_profile'),
    path('plans', views.plans, name="plans"),
    path('ref', views.ref, name="ref"),
    # path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('forgetpassword', forgetpassword, name='forgetpassword'),
    path('resetpassword_validate/<uidb64>/<token>/', resetpassword_validate, name='resetpassword_validate'),
    path('resetpassword', resetpassword, name='resetpassword'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
