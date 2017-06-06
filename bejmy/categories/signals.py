from . import initial
from .models import Category
from django.db import transaction


def _create_categories(tree, user, transaction_type, parent=None):

    for name, children in tree:
        category = Category(
            parent=parent,
            user=user,
            name=name,
            transaction_type=transaction_type
        )
        category.save()
        _create_categories(children, user, transaction_type, category)


def create_initial_categories(sender, instance, created, **kwargs):

    if created:
        with transaction.atomic():
            _create_categories(initial.withdrawal, instance,
                               transaction_type=Category.TRANSACTION_WITHDRAWAL)
            _create_categories(initial.deposit, instance,
                               transaction_type=Category.TRANSACTION_DEPOSIT)
