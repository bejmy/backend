import operator

from django.db.models import F
from django.db.models.signals import pre_save, pre_delete, post_save
from django.core.signals import request_started
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import ugettext as _

from bejmy.accounts.models import Account
from bejmy.transactions.models import Transaction


@receiver(post_save, sender=Account)
def create_initial_balancing_transaction(sender, instance, created, **kwags):
    transaction = Transaction()
    transaction.user = instance.user
    transaction.description = _('Initial balance')
    transaction.balanced = True
    transaction.balanced_at = timezone.now()

    transaction.amount = abs(instance.balance_initial)
    if instance.balance > 0:
        transaction.destination = instance
    else:
        transaction.source = instance

    transaction.save()


def __operate_account(account, transaction, op):
    amount = transaction.amount
    kwargs = {}

    field = 'balance_planned'
    kwargs.update({field: op(F(field), amount)})

    field = 'balance_registered'
    if transaction.status >= transaction.STATUS_REGISTERED:
        kwargs.update({field: op(F(field), amount)})

    field = 'balance'
    if transaction.status == transaction.STATUS_BALANCED:
        kwargs.update({field: op(F(field), amount)})

    Account.objects.filter(pk=account.pk).update(**kwargs)


def _add_transaction(account, transaction):
    __operate_account(account, transaction, operator.add)


def _subtract_transaction(account, transaction):
    __operate_account(account, transaction, operator.sub)


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


@receiver(request_started)
def register_planned_transactions(sender, **kwargs):
    # poor asynchronous task execution :D
    now = timezone.now()
    queryset = Transaction.objects.filter(
        status=Transaction.STATUS_PLANNED,
        datetime__lte=now)
    if queryset.exists():
        for transaction in queryset.all():
            print(transaction)
            transaction.save()
