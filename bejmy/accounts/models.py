from django.db import models
from django.utils.translation import ugettext_lazy as _


class Account(models.Model):
    user = models.ForeignKey(
        'users.User',
        verbose_name=_("user"),
        related_name='accounts',
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
    order = models.PositiveSmallIntegerField(
        default=0,
        verbose_name=_(u"order"),
    )
    uses = models.PositiveIntegerField(
        default=0,
        verbose_name=_(u"uses"),
    )
    account_number = models.CharField(
        max_length=255,
        verbose_name=_("account number"),
        blank=True,
        null=True,
        unique=True,
    )

    class Meta:
        verbose_name = _("account")
        verbose_name_plural = _("accounts")
        ordering = ['order', '-uses']

    def __str__(self):
        return "{self.user} / {self.name} ({self.balance})".format(self=self)

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)
