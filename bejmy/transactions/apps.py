from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class TransactionsConfig(AppConfig):
    name = 'bejmy.transactions'
    category = 'transactions'
    verbose_name = _("transactions")

    def ready(self):
        # apply signal receivers after all apps are ready
        import bejmy.transactions.receivers  # noqa
