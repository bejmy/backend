from django.conf.urls import url, include
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView, View
from django.http import HttpResponse


class FaviconView(View):
    def get(self, request):
        response = HttpResponse(
            content=open('bejmy/static/favicons/favicon.ico', 'rb'),  # FIXME
            content_type='image/x-icon',
        )
        return response


admin.site.site_title = _('Bejmy site admin')
admin.site.site_header = _('Bejmy administration')
admin.site.index_title = _('Bejmy administration')


urlpatterns = [
    # url(r'^sitemap\.xml$', sitemap, name='sitemap-xml'),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^admin/', admin.site.urls),
    url(r'^robots\.txt$', TemplateView.as_view(
        template_name='robots.txt', content_type='text/plain')),
    url(r'^browserconfig\.xml$', TemplateView.as_view(
        template_name='browserconfig.xml', content_type='application/xml')),
    url(r'^manifest\.json$', TemplateView.as_view(
        template_name='manifest.json', content_type='application/json')),
    url(r'^favicon\.ico$', FaviconView.as_view()),
]
