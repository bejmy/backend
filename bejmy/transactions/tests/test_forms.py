from django.test import TestCase
from django import forms
from unittest.mock import MagicMock

from bejmy.transactions.forms import TransactionForm


class TransactionFormTest(TestCase):

    def test_transaction_form_setup_facade(self):
        TransactionForm._set_source_initial = MagicMock()
        TransactionForm._set_balanced_initial = MagicMock()
        TransactionForm._set_categories_choices = MagicMock()
        TransactionForm._set_source_choices = MagicMock()
        TransactionForm._set_destination_choices = MagicMock()

        TransactionForm()

        assert TransactionForm._set_source_initial.called
        assert TransactionForm._set_balanced_initial.called
        assert TransactionForm._set_categories_choices.called
        assert TransactionForm._set_source_choices.called
        assert TransactionForm._set_destination_choices.called

    def test_set_source_initial_selected(self):
        form = MagicMock()
        source = MagicMock()
        form.user.settings.default_source_account = source
        form.user.settings.default_source_account_most_used = False

        TransactionForm._set_source_initial(form)
        assert form.fields['source'].initial == source

    def test_set_source_initial_most_used(self):
        form = MagicMock()
        source = MagicMock()
        form.user.accounts.first.return_value = source
        form.user.settings.default_source_account = None
        form.user.settings.default_source_account_most_used = True

        TransactionForm._set_source_initial(form)
        assert form.fields['source'].initial == source

    def test_set_balanced_initial(self):
        form = MagicMock()
        form.user.settings.default_balanced = True
        form.fields = {'balanced': MagicMock()}
        TransactionForm._set_balanced_initial(form)
        assert form.fields['balanced'].initial is True

    def test_set_categories_choices(self):
        form = MagicMock()
        categories = MagicMock()
        form.user.categories.all.return_value = categories
        form.fields = {'category': MagicMock()}

        TransactionForm._set_categories_choices(form)
        assert form.fields['category'].queryset == categories

    def test_set_source_choices(self):
        form = MagicMock()
        accounts = MagicMock()
        form.user.accounts.all.return_value = accounts
        form.fields = {'source': MagicMock()}

        TransactionForm._set_source_choices(form)
        assert form.fields['source'].queryset == accounts

    def test_set_destination_choices(self):
        form = MagicMock()
        accounts = MagicMock()
        form.user.accounts.all.return_value = accounts
        form.fields = {'destination': MagicMock()}

        TransactionForm._set_destination_choices(form)
        assert form.fields['destination'].queryset == accounts

    def test_clean_accounts(self):
        form = MagicMock()
        form.cleaned_data = {
            'destination': MagicMock(),
            'source': MagicMock(),
        }
        TransactionForm.clean_accounts(form)

    def test_clean_accounts_source_only(self):
        form = MagicMock()
        form.cleaned_data = {
            'destination': None,
            'source': MagicMock(),
        }
        TransactionForm.clean_accounts(form)

    def test_clean_accounts_destination_only(self):
        form = MagicMock()
        form.cleaned_data = {
            'destination': MagicMock(),
            'source': None,
        }
        TransactionForm.clean_accounts(form)

    def test_clean_accounts_none(self):
        form = MagicMock()
        form.cleaned_data = {
            'destination': None,
            'source': None,
        }
        with self.assertRaises(forms.ValidationError):
            TransactionForm.clean_accounts(form)

    def test_clean_accounts_the_same(self):
        form = MagicMock()
        account = MagicMock()
        form.cleaned_data = {
            'destination': account,
            'source': account,
        }
        with self.assertRaises(forms.ValidationError):
            TransactionForm.clean_accounts(form)

    def test_clean_facade(self):
        form = MagicMock()
        form.clean_accounts = MagicMock()

        TransactionForm.clean(form)

        assert form.clean_accounts.called
