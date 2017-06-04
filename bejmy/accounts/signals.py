from django.db.models import F

from bejmy.accounts.models import Account
from bejmy.transactions.models import Transaction


def _add_transaction(account, transaction):
    Account.objects.filter(pk=account.pk) \
       .update(balance=F('balance') + transaction.amount)


def _subtract_transaction(account, transaction):
    Account.objects.filter(pk=account.pk) \
       .update(balance=F('balance') - transaction.amount)


def _apply_transaction(transaction):
    if transaction.source:
        _subtract_transaction(transaction.source, transaction)

    if transaction.destination:
        _add_transaction(transaction.destination, transaction)


def _remove_transaction(transaction):
    if transaction.source:
        _add_transaction(transaction.source, transaction)

    if transaction.destination:
        _subtract_transaction(transaction.destination, transaction)



def update_account_balance(sender, instance, **kwargs):
    if instance.pk:
        old_instance = Transaction.objects.get(pk=instance.pk)
        _remove_transaction(old_instance)

    _apply_transaction(instance)


def update_account_balance_on_delete(sender, instance, **kwargs):
    _remove_transaction(instance)
