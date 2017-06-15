from decimal import Decimal

from django.test import TestCase
from django.utils import timezone

from bejmy.accounts.models import Account
from bejmy.transactions.models import Transaction
from bejmy.transactions.receivers import register_planned_transactions
from bejmy.users.models import User


class UpdateAccountTest(TestCase):
    # TODO
    pass


class InitialTransactionTest(TestCase):
    def setUp(self):
        self.user = User(
            username="test@user.com",
            email="test@user.com",
        )
        self.user.save()

    def test_create_initial_balancing_transaction(self):
        account = Account(
            user=self.user,
            name="Test Destination Account",
        )
        account.save()

        transaction = Transaction.objects.get(destination=account)
        self.assertEqual(transaction.amount, 0)

    def test_create_initial_balancing_transaction_positive_balance(self):
        balance_initial = 123
        account = Account(
            user=self.user,
            name="Test Destination Account",
            balance_initial=balance_initial,
        )
        account.save()

        transaction = Transaction.objects.get(destination=account)
        self.assertEqual(transaction.amount, balance_initial)

    def test_create_initial_balancing_transaction_negative_balance(self):
        balance_initial = -123
        account = Account(
            user=self.user,
            name="Test Destination Account",
            balance_initial=balance_initial,
        )
        account.save()

        transaction = Transaction.objects.get(source=account)
        self.assertEqual(transaction.amount, abs(balance_initial))


class RegisterPlannedTransactionsTest(TestCase):
    def setUp(self):
        pass

    def test_receiver_updates_transaction(self):
        user = User(
            username="test@user.com",
            email="test@user.com",
        )
        user.save()

        account = Account(
            user=user,
            name="Test Account",
        )
        account.save()

        now = timezone.now()

        transaction = Transaction(
            user=user,
            amount=Decimal('123.45'),
            description="Test description",
            source=account,
            datetime=now + timezone.timedelta(days=1),
        )
        transaction.save()

        self.assertEqual(transaction.status, Transaction.STATUS_PLANNED)

        import bejmy.transactions.receivers
        bejmy.transactions.receivers.timezone.now = \
            lambda: now + timezone.timedelta(days=2)
        import bejmy.transactions.models
        bejmy.transactions.models.timezone.now = \
            lambda: now + timezone.timedelta(days=2)
        register_planned_transactions()

        transaction = Transaction.objects.get(pk=transaction.pk)
        self.assertEqual(transaction.status, Transaction.STATUS_REGISTERED)
