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
        related_name='transactions_as_source',
        verbose_name=_("source"),
        blank=True,
        null=True
    )
    destination = models.ForeignKey(
        'accounts.Account',
        related_name='transactions_as_destination',
        verbose_name=_("destination"),
        blank=True,
        null=True
    )
    amount = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        verbose_name=_("amount"),
        default=0
    )
    description = models.CharField(
        max_length=255,
        blank=True,
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
        blank=True,
        choices=TRANSACTION_CHOICES,
        verbose_name=_("transaction type")
    )
    label = TreeForeignKey(
        'labels.Label',
        verbose_name=_("label"),
        null=True
    )

    class Meta:
        verbose_name = _("transaction")
        verbose_name_plural = _("transactions")

    def __str__(self):
        return f"{self.description or self.label} ({self.amount})"

    def save(self, *args, **kwargs):
        if self.source and self.destination:
            self.transaction_type = Transaction.TRANSACTION_TRANSFER
        elif self.source:
            self.transaction_type = Transaction.TRANSACTION_WITHDRAWAL
        elif self.destination:
            self.transaction_type = Transaction.TRANSACTION_DEPOSIT
        super().save(*args, **kwargs)
