from . import initial
from .models import Label


def create_initial_labels(user_model, user, created, **kwargs):

    Label.objects.all().delete()

    def create_labels(tree, transaction_type, parent=None):
        for name, children in tree:
            label = Label(
                parent=parent,
                user=user,
                name=name,
                transaction_type=transaction_type
            )
            label.save()
            create_labels(children, transaction_type, label)

    create_labels(initial.withdrawal, transaction_type=Label.TRANSACTION_WITHDRAWAL)
