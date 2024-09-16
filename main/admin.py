from django.contrib import admin
from .models import *

# Register your models here.
class ContactAdmin(admin.ModelAdmin):
    list_display = ('full_name','email',)
    list_display_links = ('full_name','email',)
    search_fields = ('full_name','email',)
    list_per_page = 25

admin.site.register(Contact,ContactAdmin)

# admin.site.register(Subscribe, SubscribeAdmin)
# admin.site.register(First_Plan)
# admin.site.register(Second_Plan)
# admin.site.register(Third_Plan)
# admin.site.register(Forth_Plan)