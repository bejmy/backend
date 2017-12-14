import csv
import decimal
import hashlib
import re
import tablib

from collections import namedtuple

from django.utils import timezone

from import_export.formats.base_formats import Format

from .models import Transaction


class MBankCSVFormat(Format):

    def get_title(self):
        return "mBank CSV"

    def can_import(self):
        return True

    def create_dataset(self, in_stream):

        fields = [
            'id',
            'user',
            'source',
            'destination',
            'amount',
            'description',
            'datetime',
            'balanced',
            'balanced_changed',
            'transaction_type',
            'category',
            'created_by',
            'created_at',
            'modified_by',
            'modified_at',
            'status',
            'tags',
            'import_hash',
        ]

        in_stream = in_stream.decode('cp1250')
        header_divider = '#Data operacji;#Data księgowania;#Opis operacji;#Tytuł;#Nadawca/Odbiorca;#Numer konta;#Kwota;#Saldo po operacji;'  # noqa
        self.header, in_stream = in_stream.split(header_divider)
        footer_divider = ';;;;;;#Saldo końcowe;'
        in_stream, _ = in_stream.split(footer_divider)

        mBankRecord = namedtuple('mBankRecord', 'transaction_date balanced_date description title party account_number amount saldo x')  # noqa

        reader = csv.reader(in_stream.splitlines(), delimiter=';')
        dataset = tablib.Dataset()

        dataset.headers = fields
        for record in map(mBankRecord._make, filter(bool, reader)):
            dataset.append([self.get_field_data(field, record) for field in fields])  # noqa

        return dataset

    def get_import_hash_field_data(self, record):
        return hashlib.sha256("".join(record).encode()).hexdigest()

    def get_field_data(self, field, record):
        return getattr(self, "get_{}_field_data".format(field))(record)

    def get_id_field_data(self, record):
        return None

    def get_user_field_data(self, record):
        return None

    @property
    def account_number(self):
        account_number = self.header.split('Numer rachunku;')[1].splitlines()[1]
        return ''.join(re.findall(r'\d+', account_number))

    def get_source_field_data(self, record):
        if self._get_amount(record) <= 0:
            return self.account_number
        # FIXME: figure out a way to properly detect and not duplicate transfers
        # else:
        #     return ''.join(re.findall(r'\d+', record.account_number))

    def get_destination_field_data(self, record):
        if self._get_amount(record) > 0:
            return self.account_number
        # FIXME: figure out a way to properly detect and not duplicate transfers
        # else:
        #     return ''.join(re.findall(r'\d+', record.account_number))

    def _get_amount(self, record):
        return decimal.Decimal(record.amount.replace(',', '.').replace(' ', ''))

    def get_amount_field_data(self, record):
        return abs(self._get_amount(record))

    def get_description_field_data(self, record):
        return "\n".join((
            record.description,
            record.title.split('DATA TRANSAKCJI: ')[0],
            record.party))

    def _get_datetime(self, string):
        return timezone.datetime.strptime(string[:10], '%Y-%m-%d')

    def get_datetime_field_data(self, record):
        try:
            string = record.title.split('DATA TRANSAKCJI: ')[1]
        except IndexError:
            string = record.transaction_date
        return self._get_datetime(string)

    def get_balanced_field_data(self, record):
        return True

    def get_balanced_changed_field_data(self, record):
        return self._get_datetime(record.balanced_date)

    def get_transaction_type_field_data(self, record):
        return None

    def get_category_field_data(self, record):
        return None

    def get_tags_field_data(self, record):
        return None

    def get_created_by_field_data(self, record):
        return None

    def get_created_at_field_data(self, record):
        return timezone.now()

    def get_modified_by_field_data(self, record):
        return None

    def get_modified_at_field_data(self, record):
        return timezone.now()

    def get_status_field_data(self, record):
        return Transaction.STATUS_BALANCED
