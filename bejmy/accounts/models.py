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

    def __str__(self):
        return f"{self.user} / {self.name}"
