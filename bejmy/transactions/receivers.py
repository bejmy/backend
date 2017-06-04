from django.db.models import F
from django.db.models.signals import pre_save, pre_delete, post_save
from django.dispatch import receiver
from django.utils.translation import ugettext as _

from bejmy.accounts.models import Account
from bejmy.transactions.models import Transaction


@receiver(post_save, sender=Account)
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

        # force save balance again because it was overwritten by
        # `update_account_balance` signal receiver
        instance.save()



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


@receiver(pre_save, sender=Transaction)
def update_account_balance(sender, instance, **kwargs):
    if instance.pk:
        old_instance = Transaction.objects.get(pk=instance.pk)
        _remove_transaction(old_instance)

    _apply_transaction(instance)


@receiver(pre_delete, sender=Transaction)
def update_account_balance_on_delete(sender, instance, **kwargs):
    _remove_transaction(instance)
