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
    balance_initial = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name=_("balance initial")
    )
    balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name=_("balance")
    )
    balance_planned = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name=_("balance planned")
    )
    balance_registered = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name=_("balance registered")
    )

    def __str__(self):
        return f"{self.name} ({self.balance})"

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)
