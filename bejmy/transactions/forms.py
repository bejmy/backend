from decimal import Decimal
from django import forms
from django.utils.translation import ugettext as _

from .models import Transaction


class TransactionAdminForm(forms.ModelForm):

    amount = forms.DecimalField(
        min_value=Decimal('0.01'),
        decimal_places=2
    )

    class Meta:
        exclude = ()
        model = Transaction

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        user = self.user
        if user.settings.default_source_account_most_used:
            source = user.accounts.first()
        else:
            source = user.settings.default_source_account
        self.fields['source'].initial = source
        self.fields['balanced'].initial = user.settings.default_balanced

        queryset = user.categories.all()
        self.fields['category'].queryset = queryset

        queryset = user.accounts.all()
        self.fields['source'].queryset = queryset
        self.fields['destination'].queryset = queryset

    def clean(self):
        source = self.cleaned_data.get('source')
        destination = self.cleaned_data.get('destination')
        if not (source or destination):
            raise forms.ValidationError(_("Account(s) not selected."))
        if source == destination:
            raise forms.ValidationError(
                _("Source and destination accounts are the same."))
        return self.cleaned_data
