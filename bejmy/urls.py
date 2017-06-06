from django.conf.urls import url, include
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

admin.site.site_title = _('Bejmy site admin')
admin.site.site_header = _('Bejmy administration')
admin.site.index_title = _('Bejmy administration')


urlpatterns = [
    # url(r'^sitemap\.xml$', sitemap, name='sitemap-xml'),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^admin/', admin.site.urls),
]
