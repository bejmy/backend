from django.contrib import admin

from bejmy.transactions.models import Transaction
from bejmy.accounts.models import Account
from bejmy.labels.models import Label
from .forms import TransactionAdminForm


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    form = TransactionAdminForm
    readonly_fields = ['user', 'transaction_type']

    def get_form(self, request, *args, **kwargs):
        form = super().get_form(request, *args, **kwargs)
        form.user = request.user
        return form

    def save_model(self, request, obj, *args, **kwargs):
        obj.user = request.user
        return super().save_model(request, obj, *args, **kwargs)

    def get_changeform_initial_data(self, request):
        return {'user': request.user}
