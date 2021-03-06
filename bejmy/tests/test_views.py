from django.test import TestCase

from bejmy.views import favicon_view


class MockRequest:
    method = 'GET'


class TestFaviconView(TestCase):

    def test_favicon_view(self):
        request = MockRequest()
        response = favicon_view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'image/x-icon')
