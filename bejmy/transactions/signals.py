from .models import Transaction
from django.utils.translation import ugettext as _


def create_initial_balancing_transaction(sender, instance, created, **kwags):
    if created and instance.balance != 0:
        transaction = Transaction()
        transaction.user = instance.user
        transaction.description = _('Initial balance')
        transaction.status = Transaction.STATUS_BALANCED
        transaction.amount = abs(instance.balance)

        if instance.balance > 0:
            transaction.destination = instance
        else:
            transaction.source = instance

        transaction.save()

        # force save balance again because it was overwritten by transaction
        # signal
        instance.save()
