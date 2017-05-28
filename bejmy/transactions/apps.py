from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class TransactionsConfig(AppConfig):
    name = 'bejmy.transactions'
    label = 'transactions'
    verbose_name = _("transactions")
