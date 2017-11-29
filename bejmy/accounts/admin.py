from django.contrib import admin

from bejmy.accounts.models import Account
from bejmy.transactions.models import Transaction
from bejmy.transactions.admin import TransactionAdminBase


class TransactionAdmin(TransactionAdminBase, admin.TabularInline):
    model = Transaction
    fk_name = 'source'

    def has_change_permission(self, obj):
        return False

    def get_formset(self, request, obj=None, **kwargs):
        self._form.user = request.user
        return super().get_formset(request, obj=None, form=self._form, **kwargs)


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'balance_planned', 'balance_registered', 'balance')
    readonly_fields = ('balance', 'balance_planned', 'balance_registered')
    inlines = [TransactionAdmin]

    def get_queryset(self, request, *args, **kwargs):
        queryset = super().get_queryset(request, *args, **kwargs)
        if not request.user.is_superuser:
            queryset = queryset.filter(user=request.user)
        return queryset
