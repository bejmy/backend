from django import forms


class TransactionAdminForm(forms.ModelForm):
    class Meta:
        model = Transaction

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        available_choices = []
        self.fields['label'].choices = available_choices
