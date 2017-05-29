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


def create_initial_labels(user_model, user, created, **kwargs):

    if created:
        _create_labels(initial.withdrawal, user,
                       transaction_type=Label.TRANSACTION_WITHDRAWAL)
