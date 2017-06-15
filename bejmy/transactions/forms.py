from decimal import Decimal
from django import forms
from django.utils.translation import ugettext as _

from .models import Transaction


class TransactionForm(forms.ModelForm):

    amount = forms.DecimalField(
        min_value=Decimal('0.01'),
        decimal_places=2
    )

    class Meta:
        exclude = ()
        model = Transaction

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._set_source_initial()
        self._set_balanced_initial()
        self._set_categories_choices()
        self._set_source_choices()
        self._set_destination_choices()

    def _set_source_initial(self):
        if self.user.settings.default_source_account_most_used:
            source = self.user.accounts.first()
        else:
            source = self.user.settings.default_source_account
        self.fields['source'].initial = source

    def _set_balanced_initial(self):
        self.fields['balanced'].initial = self.user.settings.default_balanced

    def _set_categories_choices(self):
        self.fields['category'].queryset = self.user.categories.all()

    def _set_source_choices(self):
        self.fields['source'].queryset = self.user.accounts.all()

    def _set_destination_choices(self):
        self.fields['destination'].queryset = self.user.accounts.all()

    def clean(self):
        source = self.cleaned_data.get('source')
        destination = self.cleaned_data.get('destination')
        if not (source or destination):
            raise forms.ValidationError(_("Account(s) not selected."))
        if source == destination:
            raise forms.ValidationError(
                _("Source and destination accounts are the same."))
        return self.cleaned_data
