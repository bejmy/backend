from django.db import models
from django.utils.translation import ugettext_lazy as _


class Account(models.Model):
    user = models.ForeignKey(
        'users.User',
        verbose_name=_("user")
    )
    name = models.CharField(
        max_length=255,
        verbose_name=_("name")
    )
    balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        editable=False,
        verbose_name=_("balance")
    )

    def __str__(self):
        return f"{self.user} / {self.name} / {self.balance}"
