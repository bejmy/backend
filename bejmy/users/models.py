from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):
    default_source_account = models.ForeignKey(
        'accounts.Account',
        blank=True,
        null=True,
        verbose_name=_('default source account'),
        related_name='+',
    )

    def __str__(self):
        return self.get_full_name() or self.email
