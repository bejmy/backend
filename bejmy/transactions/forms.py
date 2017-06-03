from django import forms
from bejmy.labels.models import Label
from bejmy.accounts.models import Account
from bejmy.users.models import User


from .models import Transaction


class TransactionAdminForm(forms.ModelForm):
    class Meta:
        exclude = ()
        model = Transaction

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        user = self.user

        queryset = Label.objects.filter(user=user)
        self.fields['label'].queryset = queryset

        queryset = Account.objects.filter(user=user)
        self.fields['source'].queryset = queryset
        self.fields['destination'].queryset = queryset
