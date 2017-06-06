from django.contrib import admin

from bejmy.accounts.models import Account


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'balance_planned', 'balance_registered', 'balance')
    readonly_fields = ('balance', 'balance_planned', 'balance_registered')
