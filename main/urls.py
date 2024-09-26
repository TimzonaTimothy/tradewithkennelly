from django.urls import path, re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from accounts.views import sign_in, sign_up

urlpatterns = [
    path('', views.home, name='home'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('plans',views.plans, name="plans"),
    path('faq',views.faq, name="faq"),
    path('services',views.services, name="services"),
    path('glossary',views.glossary, name="glossary"),
    path('market_data',views.market_data, name="market_data"),
    path('terms',views.terms, name="terms"),
    path('privacy',views.privacy, name="privacy"),
    path('sign_up', sign_up, name='sign_up'),
    path('sign_in', sign_in, name='sign_in'),
    path('logout',views.user_logout, name="logout"),
    path('newsletter-sub', views.newsletter_sub, name='newsletter-sub'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = 'main.views.handler404'
handler500 = 'main.views.handler500'