from django.db.models import F

from .models import Account
from bejmy.transactions.models import Transaction


def update_account_balance(sender, instance, **kwags):
    if instance.pk:
        # its an existing transaction - undo account balance update
        old_instance = Transaction.objects.get(pk=instance.pk)

        if old_instance.source:
            Account.objects.filter(pk=old_instance.source.pk) \
               .update(balance=F('balance') + old_instance.amount)

        if old_instance.destination:
            Account.objects.filter(pk=old_instance.destination.pk) \
               .update(balance=F('balance') - old_instance.amount)

    if instance.source:
        Account.objects.filter(pk=instance.source.pk) \
           .update(balance=F('balance') - instance.amount)

    if instance.destination:
        Account.objects.filter(pk=instance.destination.pk) \
           .update(balance=F('balance') + instance.amount)
