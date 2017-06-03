from .models import Transaction
from django.utils.translation import ugettext as _


def create_initial_balancing_transaction(sender, instance, created, **kwags):
    if created and instance.balance != 0:
        transaction = Transaction()
        transaction.user = instance.user
        transaction.destination = instance
        transaction.description = _('Initial balance')
        transaction.amount = instance.balance
        transaction.status = Transaction.STATUS_BALANCED
        transaction.transaction_type = Transaction.TRANSACTION_BALANCE
        transaction.save()
