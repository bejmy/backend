from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class AccountsConfig(AppConfig):
    name = 'bejmy.accounts'
    category = 'accounts'
    verbose_name = _("accounts")
