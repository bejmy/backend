from django.test import TestCase
from django.contrib.admin.sites import AdminSite

from bejmy.users.models import User
from bejmy.users.admin import UserAdmin


class MockRequest:
    pass


# class MockSuperUser:
#     def has_perm(self, perm):
#         return True


request = MockRequest()
# request.user = MockSuperUser()


class UserAdminTests(TestCase):

    def setUp(self):
        self.user = User(
            username="testuser",
            email="test@user.com",
        )
        self.site = AdminSite()

    def test_get_fieldsets_has_extra_fieldset(self):
        a = UserAdmin(User, self.site)
        self.assertTrue(a.fieldset_extra in a.get_fieldsets(request))
