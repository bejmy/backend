from django.http import HttpResponse
from django.views.generic import View


class FaviconView(View):
    def get(self, request):
        response = HttpResponse(
            content=open('bejmy/static/favicons/favicon.ico', 'rb'),  # FIXME
            content_type='image/x-icon',
        )
        return response


favicon_view = FaviconView.as_view()
