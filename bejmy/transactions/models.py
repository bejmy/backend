from django.db import models
from django.utils import timezone
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
    category = TreeForeignKey(
        'categories.Category',
        verbose_name=_("category"),
        null=True
    )
    # created_by = models.ForeignKey(
    #     'users.User',
    #     verbose_name=_('created by')
    # )
    created_at = models.DateTimeField(
        verbose_name=_('created at')
    )
    # modified_by = models.ForeignKey(
    #     'users.User',
    #     verbose_name=_('modified by'),
    # )
    modified_at = models.DateTimeField(
        verbose_name=_('modified at'),
    )

    class Meta:
        verbose_name = _("transaction")
        verbose_name_plural = _("transactions")

    def __str__(self):
        return f"{self.description or self.category} ({self.amount})"

    def get_transaction_type(self):
        if self.source and self.destination:
            transaction_type = Transaction.TRANSACTION_TRANSFER
        elif self.source:
            transaction_type = Transaction.TRANSACTION_WITHDRAWAL
        elif self.destination:
            transaction_type = Transaction.TRANSACTION_DEPOSIT
        return transaction_type

    def save(self, *args, **kwargs):

        # set created and modified times
        if not self.id:
            self.created_at = timezone.now()
        self.modified_at = timezone.now()

        self.transaction_type = self.get_transaction_type()
        super().save(*args, **kwargs)
