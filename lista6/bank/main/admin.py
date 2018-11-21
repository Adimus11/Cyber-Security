from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import BankUser

@admin.register(BankUser)
class BankUserAdminAdmin(admin.ModelAdmin):
    fields = ('username', 'email', 'password', 'balance')