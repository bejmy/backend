from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class UsersConfig(AppConfig):
    name = 'bejmy.users'
    category = 'users'
    verbose_name = _("users")
