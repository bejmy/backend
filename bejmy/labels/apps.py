from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save


class LabelsConfig(AppConfig):
    name = 'bejmy.labels'
    label = 'labels'
    verbose_name = _("labels")

    def ready(self):
        from .signals import create_initial_labels
        post_save.connect(create_initial_labels, sender='users.User',
                          dispatch_uid='create_initial_labels')
