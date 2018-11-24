from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import BankUser, Transfer

@admin.register(BankUser)
class BankUserAdminAdmin(admin.ModelAdmin):
    fields = ('balance', 'available_founds' )
    readonly_fields = ('username', 'email', 'password')


@admin.register(Transfer)
class TransferAdmin(admin.ModelAdmin):
    readonly_fields = ('sender', 'receiver', 'amount', 'date', 'is_staged')
