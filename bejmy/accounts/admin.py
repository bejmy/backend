from django.contrib import admin

from bejmy.accounts.models import Account


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'balance_planned', 'balance_registered', 'balance')
    readonly_fields = ('balance', 'balance_planned', 'balance_registered')

    def get_queryset(self, request, *args, **kwargs):
        queryset = super().get_queryset(request, *args, **kwargs)
        if not request.user.is_superuser():
            queryset = queryset.filter(user=request.user)
        return queryset
