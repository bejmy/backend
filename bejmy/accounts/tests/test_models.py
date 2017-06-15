from unittest.mock import MagicMock

from django.test import TestCase

from bejmy.accounts.models import Account
from bejmy.users.models import User


class AccountModelTestCase(TestCase):
    def test_str_contains_user(self):
        user = User(
            username="testuser",
            email="test@user.com",
        )
        account = Account(user=user)
        assert str(user) in str(account)

    def test_str_contains_name(self):
        user = User(
            username="testuser",
            email="test@user.com",
        )
        name = str(MagicMock())
        account = Account(
            user=user,
            name=name
        )
        assert name in str(account)

    def test_str_contains_balance(self):
        user = User(
            username="testuser",
            email="test@user.com",
        )

        account = Account(
            user=user,
            balance=123
        )
        assert '123' in str(account)
