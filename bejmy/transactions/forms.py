from decimal import Decimal
from django import forms
from django.utils.translation import ugettext as _

from bejmy.accounts.models import Account
from bejmy.categories.models import Category


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

        queryset = Category.objects.filter(user=user)
        self.fields['category'].queryset = queryset

        queryset = Account.objects.filter(user=user)
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
