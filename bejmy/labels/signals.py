from . import initial
from .models import Label


def _create_labels(tree, user, transaction_type, parent=None):

    for name, children in tree:
        label = Label(
            parent=parent,
            user=user,
            name=name,
            transaction_type=transaction_type
        )
        label.save()
        _create_labels(children, transaction_type, label)


def create_initial_labels(sender, instance, created, **kwargs):
    return

    if created:
        _create_labels(initial.withdrawal, instance,
                       transaction_type=Label.TRANSACTION_WITHDRAWAL)
