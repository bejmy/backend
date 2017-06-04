from decimal import Decimal
from django.test import TestCase
from bejmy.transactions.models import Transaction
from bejmy.users.models import User
from bejmy.accounts.models import Account
from bejmy.labels.models import Label


class TransactionModelTestCase(TestCase):
    def setUp(self):
        user = User(
            username="test@user.com",
            email="test@user.com",
        )
        user.save()

        self.source_account = Account(
            user=user,
            name="Test Source Account",
        )
        self.source_account.save()

        self.destination_account = Account(
            user=user,
            name="Test Destination Account",
        )
        self.destination_account.save()

        self.label = Label(
            user=user,
            name="Test Label",
            transaction_type=Label.TRANSACTION_DEPOSIT
        )
        self.label.save()

        self.transaction = Transaction(
            user=user,
            amount=Decimal('123.45'),
            description="Test description",
            status=Transaction.STATUS_BALANCED,
        )

    def test_save_sets_transaction_type_withdrawal(self):
        self.transaction.source = self.source_account
        self.transaction.save()
        self.assertEqual(
            self.transaction.transaction_type,
            Transaction.TRANSACTION_WITHDRAWAL)

    def test_save_sets_transaction_type_deposit(self):
        self.transaction.destination = self.destination_account
        self.transaction.save()
        self.assertEqual(
            self.transaction.transaction_type,
            Transaction.TRANSACTION_DEPOSIT)

    def test_save_sets_transaction_type_transfer(self):
        self.transaction.source = self.source_account
        self.transaction.destination = self.destination_account
        self.transaction.save()
        self.assertEqual(
            self.transaction.transaction_type,
            Transaction.TRANSACTION_TRANSFER)

    def test_cast_to_string_has_description_and_amount(self):
        self.assertEqual(
            str(self.transaction),
            f"{self.transaction.description} ({self.transaction.amount})")

    def test_cast_to_string_has_label_and_amount(self):
        self.transaction.description = ''
        self.transaction.label = self.label
        self.assertEqual(
            str(self.transaction),
            f"{self.transaction.label} ({self.transaction.amount})")
