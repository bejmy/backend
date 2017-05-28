from django.contrib import admin

from bejmy.accounts.models import Account


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    pass
