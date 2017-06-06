from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save


class CategoriesConfig(AppConfig):
    name = 'bejmy.categories'
    category = 'categories'
    verbose_name = _("categories")

    def ready(self):
        from .signals import create_initial_categories
        post_save.connect(create_initial_categories, sender='users.User',
                          dispatch_uid='create_initial_categories')
