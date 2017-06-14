from django.test import TestCase
from bejmy.users.models import User, Settings


class UserModelTestCase(TestCase):
    def setUp(self):
        pass

    def test_str_returns_username(self):
        user = User(
            username="testuser",
            email="test@user.com",
        )
        self.assertEqual(str(user), user.username)

    def test_str_returns_full_name(self):
        user = User(
            username="testuser",
            email="test@user.com",
            first_name='First',
            last_name='Last',
        )
        self.assertEqual(str(user), user.get_full_name())


class SettingsModelTestCase(TestCase):
    def setUp(self):
        self.user = User(
            username="testuser",
            email="test@user.com",
        )

    def test_str_contains_user_str(self):
        settings = Settings(
            user=self.user
        )
        assert str(self.user) in str(settings)
