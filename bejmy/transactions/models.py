from django.db import models
from django.utils.translation import ugettext_lazy as _

from mptt.fields import TreeForeignKey


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
    STATUS_PLANNED = 1
    STATUS_REGISTERED = 2
    STATUS_BALANCED = 3
    STATUS_DEFAULT = STATUS_REGISTERED
    STATUS_CHOICES = (
        (STATUS_PLANNED, _("planned")),
        (STATUS_REGISTERED, _("registered")),
        (STATUS_BALANCED, _("balanced")),
    )
    status = models.PositiveSmallIntegerField(
        choices=STATUS_CHOICES,
        default=STATUS_DEFAULT
    )
    TRANSACTION_WITHDRAWAL = 1
    TRANSACTION_DEPOSIT = 2
    TRANSACTION_TRANSFER = 3
    TRANSACTION_CHOICES = (
        (TRANSACTION_WITHDRAWAL, _("withdrawal")),
        (TRANSACTION_DEPOSIT, _("deposit")),
        (TRANSACTION_TRANSFER, _("transfer")),
    )
    transaction_type = models.PositiveSmallIntegerField(
        choices=TRANSACTION_CHOICES
    )
    label = TreeForeignKey(
        'labels.Label',
        verbose_name=_("label")
    )

    class Meta:
        verbose_name = _("transaction")
        verbose_name_plural = _("transactions")
        unique_together = [('source', 'destination')]

    def __str__(self):
        return self.description
