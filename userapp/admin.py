from django.contrib import admin
from .models import UserDetails, UserBankDetails
# Register your models here.
admin.site.register(UserDetails)
admin.site.register(UserBankDetails)