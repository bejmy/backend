from django.apps import AppConfig
from django.db.models.signals import pre_save
from django.utils.translation import ugettext_lazy as _


class AccountsConfig(AppConfig):
    name = 'bejmy.accounts'
    label = 'accounts'
    verbose_name = _("accounts")

    def ready(self):
        from .signals import update_account_balance
        pre_save.connect(
                update_account_balance,
                sender='transactions.Transaction',
                dispatch_uid='update_account_balance')
