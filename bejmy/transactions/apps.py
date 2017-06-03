from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save


class TransactionsConfig(AppConfig):
    name = 'bejmy.transactions'
    label = 'transactions'
    verbose_name = _("transactions")

    def ready(self):
        from .signals import create_initial_balancing_transaction
        post_save.connect(
                create_initial_balancing_transaction,
                sender='accounts.Account',
                dispatch_uid='create_initial_balancing_transaction')
