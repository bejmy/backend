from django.contrib import admin

from bejmy.transactions.models import Transaction
from bejmy.accounts.models import Account
from bejmy.labels.models import Label


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    def get_form(self, request, *args, **kwargs):
        form = super().get_form(request, *args, **kwargs)

        form.base_fields['user'].choices = [
            (request.user.pk, request.user)
        ]

        queryset = Label.objects.filter(user=request.user)
        available_choices = ((label.pk, label) for label in queryset)
        form.base_fields['label'].choices = available_choices

        queryset = Account.objects.filter(user=request.user)
        available_choices = [(account.pk, account) for account in queryset]
        form.base_fields['source'].choices = available_choices
        form.base_fields['destination'].choices = available_choices

        return form
