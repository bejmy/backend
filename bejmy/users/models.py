from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):

    def __str__(self):
        return self.get_full_name() or self.username


class Settings(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='settings',
    )
    default_source_account = models.ForeignKey(
        'accounts.Account',
        blank=True,
        null=True,
        verbose_name=_('default source account'),
        related_name='+',
    )
    default_source_account_most_used = models.BooleanField(
        default=False,
        verbose_name=_("default source account most used"),
    )
    default_balanced = models.BooleanField(
        default=False,
        verbose_name=_("default balanced"),
    )

    class Meta:
        verbose_name = _(u"settings")
        verbose_name_plural = _(u"settings")

    def __str__(self):
        return str(_("{self.user} settings".format(self=self)))
