from collections import defaultdict

from django.core.signals import request_started
from django.db.models import Sum, Value, Count
from django.db.models.functions import Coalesce
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import ugettext as _

from bejmy.accounts.models import Account
from bejmy.transactions.models import Transaction


@receiver(post_save, sender=Account)
def create_initial_balancing_transaction(sender, instance, created, **kwags):
    if created:
        transaction = Transaction()
        transaction.user = instance.user
        transaction.description = _('Initial balance')
        transaction.balanced = True
        transaction.balanced_at = timezone.now()

        transaction.amount = abs(instance.balance_initial)
        if instance.balance_initial >= 0:
            transaction.destination = instance
        else:
            transaction.source = instance

        transaction.save()


@receiver(post_delete, sender=Transaction)
@receiver(post_save, sender=Transaction)
def update_account(sender, instance, **kwargs):
    """Update account balance and usage data."""
    # keep it ordered, order used later in make balances cumulative
    status_field_map = {
        Transaction.STATUS_BALANCED: 'balance',
        Transaction.STATUS_REGISTERED: 'balance_registered',
        Transaction.STATUS_PLANNED: 'balance_planned',
    }
    account_balance_data = defaultdict(
        lambda: {field: 0 for field in status_field_map.values()})
    account_usage_data = defaultdict(int)

    # get transaction balance data
    queryset = Transaction.objects.filter(user=instance.user)
    queryset = queryset.values('source_id', 'destination_id', 'status')
    results = queryset.annotate(
        amount=Coalesce(Sum('amount'), Value(0)),
        count=Count('pk'))

    # populate data dicts with data
    for result in results:
        field = status_field_map[result['status']]
        source_id = result['source_id']
        destination_id = result['destination_id']
        if source_id is not None:
            # withdrawal
            account_balance_data[source_id][field] -= result['amount']
            account_usage_data[source_id] += result['count']
        if destination_id is not None:
            # deposit
            account_balance_data[destination_id][field] += result['amount']
            account_usage_data[destination_id] += result['count']

    # make account balance data cumulative, order of fields is important
    for account_pk in account_balance_data:
        balance = 0
        for field, value in account_balance_data[account_pk].items():
            balance += value
            account_balance_data[account_pk][field] = balance

    # update database
    for account_pk, data in account_balance_data.items():
        Account.objects.filter(pk=account_pk).update(
            uses=account_usage_data[account_pk], **data)


@receiver(request_started)
def register_planned_transactions(*args, **kwargs):
    # poor asynchronous task execution :D
    now = timezone.now()
    transactions = Transaction.objects.filter(
        status=Transaction.STATUS_PLANNED,
        datetime__lte=now)

    # TODO: figure out if there's a better way to update transaction status and
    # update accounts balances
    for transaction in transactions:
        transaction.save()
