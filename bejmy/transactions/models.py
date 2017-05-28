from django.db import models
from django.utils.translation import ugettext_lazy as _


class Transaction(models.Model):
    user = models.ForeignKey(
        'users.User',
        verbose_name=_("user")
    )
    source = models.ForeignKey(
        'accounts.Account',
        related_name='transaction_as_source',
        verbose_name=_("source"),
        blank=True,
        null=True
    )
    destination = models.ForeignKey(
        'accounts.Account',
        related_name='transaction_as_destination',
        verbose_name=_("destination"),
        blank=True,
        null=True
    )
    amount = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        verbose_name=_("amount")
    )
    description = models.CharField(
        max_length=255,
        verbose_name=_("description")
    )

    class Meta:
        verbose_name = _("transaction")
        verbose_name_plural = _("transactions")
        unique_together = [('source', 'destination')]

    def __str__(self):
        return self.description
