from django.db import models
from django.utils.translation import ugettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):
    parent = TreeForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='children',
        db_index=True
    )
    user = models.ForeignKey(
        'users.User',
        verbose_name=_("user")
    )
    name = models.CharField(
        max_length=255,
        verbose_name=_("name")
    )
    TRANSACTION_WITHDRAWAL = 1
    TRANSACTION_DEPOSIT = 2
    TRANSACTION_CHOICES = (
        (TRANSACTION_WITHDRAWAL, _("withdrawal")),
        (TRANSACTION_DEPOSIT, _("deposit")),
    )
    transaction_type = models.PositiveSmallIntegerField(
        choices=TRANSACTION_CHOICES
    )

    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")

    def __str__(self):
        return f"{self.name}"
