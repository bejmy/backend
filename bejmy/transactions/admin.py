from django.contrib import admin
from django.contrib.admin.views.main import ChangeList
from django.db.models import DecimalField, Sum
from django.db.models.functions import Coalesce
from django.utils.translation import ugettext as _

from mptt.admin import TreeRelatedFieldListFilter
from rangefilter.filter import DateRangeFilter

from bejmy.transactions.forms import TransactionForm
from bejmy.transactions.models import Transaction
from bejmy.categories.models import Category

from import_export import resources
from import_export.admin import ImportExportModelAdmin

from bejmy.transactions.formats import MBankCSVFormat


class TransactionResource(resources.ModelResource):

    def skip_row(self, instance, original):
        if original.pk:
            return True

    def before_import_row(self, row, **kwargs):
        user_pk = kwargs['user'].pk
        if row['user'] is None:
            row['user'] = user_pk
        if row['created_by'] is None:
            row['created_by'] = user_pk
        if row['modified_by'] is None:
            row['modified_by'] = user_pk

        from bejmy.accounts.models import Account

        if row['source']:
            try:
                source = Account.objects.get(user_id=user_pk, account_number=row['source']) # noqa
            except Account.DoesNotExist:
                row['source'] = None
            else:
                row['source'] = source.pk

        if row['destination']:
            try:
                destination = Account.objects.get(user_id=user_pk, account_number=row['destination'])  # noqa
            except Account.DoesNotExist:
                row['destination'] = None
            else:
                row['destination'] = destination.pk

    class Meta:
        model = Transaction
        import_id_fields = ['import_hash']
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


class CategoryFilter(TreeRelatedFieldListFilter):
    mptt_level_indent = 3
    template = 'admin/filter_dropdown.html'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # fix
        self.lookup_kwarg = self.changed_lookup_kwarg

    def field_choices(self, field, request, model_admin):
        """Use existing `padding_style` as prefix for select options."""
        field.rel.limit_choices_to = {'user': request.user}
        choices = []
        original_choices = super().field_choices(field, request, model_admin)
        for pk, val, padding_style in original_choices:
            a = padding_style.index(':') + 1
            b = padding_style.index('px')
            choices.append((pk, val, '-' * int(padding_style[a:b])))
        return choices


class TransactionChangeList(ChangeList):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.get_summary()
        self.get_categories()

    def get_categories(self):
        queryset = self.queryset._clone().filter(
            transaction_type=Transaction.TRANSACTION_WITHDRAWAL)
        queryset = queryset.values_list('category')
        queryset = queryset.annotate(amount=Sum('amount'))
        category_amount = queryset.order_by('-amount')
        if category_amount:
            categories = Category.objects.in_bulk(
                filter(None, tuple(zip(*category_amount))[0]))
            self.categories = ((categories.get(pk, 'Other'), amount) for pk, amount in category_amount)  # noqa
        else:
            self.categories = ()

    def _get_summary_entry(self, summary, key, **filter_kwargs):
        queryset = self.queryset._clone().filter(**filter_kwargs)
        field = DecimalField(max_digits=9, decimal_places=2)
        aggregate_kwargs = {
            key: Coalesce(Sum('amount', output_field=field), 0)
        }
        summary.update(queryset.aggregate(**aggregate_kwargs))
        return summary

    def get_summary(self):
        queries = {
            _('Planned'): {'status': Transaction.STATUS_PLANNED},
            _('Registered'): {'status': Transaction.STATUS_REGISTERED},
            _('Balanced'): {'status': Transaction.STATUS_BALANCED},
            _('Total'): {},
        }
        self.summary = []
        for name, filters in queries.items():
            self.summary.append(self._get_single_summary(name, **filters))

    def _get_single_summary(self, name, **extra_filters):
        summary = {}
        summary['name'] = name
        query = {
            'withdrawal': {
                'transaction_type': Transaction.TRANSACTION_WITHDRAWAL
            },
            'deposit': {
                'transaction_type': Transaction.TRANSACTION_DEPOSIT,
            },
            'transfer': {
                'transaction_type': Transaction.TRANSACTION_TRANSFER,
            },
        }

        for key, filters in query.items():
            if extra_filters is not None:
                filters.update(extra_filters)
            self._get_summary_entry(summary, key, **filters)

        summary['total'] = summary['deposit'] - summary['withdrawal']

        return summary


class TransactionAdminBase:
    _form = TransactionForm

    fieldset_base = (None, {
        'fields': (
            'source',
            'destination',
            'amount',
            'description',
            'datetime',
            'balanced',
            'category',
            'tags',
        )
    })

    def get_fieldsets(self, request, obj=None):
        fieldsets = [self.fieldset_base]
        return fieldsets


@admin.register(Transaction)
class TransactionAdmin(TransactionAdminBase, ImportExportModelAdmin):
    change_list_template = 'admin/transactions/transaction/change_list.html'

    resource_class = TransactionResource
    formats = [MBankCSVFormat]

    def get_changelist(self, request, **kwargs):
        return TransactionChangeList

    fieldset_info = ('Info', {
        'fields': (
            'status',
            'transaction_type',
            'user',
            'balanced_changed',
            'created_at',
            'created_by',
            'modified_at',
            'modified_by',
        ),
    })

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if obj is not None:
            fieldsets.append(self.fieldset_info)
        return fieldsets

    def get_form(self, request, *args, **kwargs):
        self._form.user = request.user
        form = super().get_form(request, *args, form=self._form)
        for field in ('source', 'destination', 'category'):
            form.base_fields[field].widget.can_add_related = False
            form.base_fields[field].widget.can_change_related = False
        return form

    list_display_links = (
        '__str__',
    )
    list_display = (
        '__str__',
        'description',
        'category',
        'tag_list',
        'balanced',
        'user',
        'status',
        'transaction_type',
        'source',
        'destination',
    )
    readonly_fields = (
        'balanced_changed',
        'created_at',
        'created_by',
        'modified_at',
        'modified_by',
        'status',
        'transaction_type',
        'user',
    )
    list_filter = (
        ('datetime', DateRangeFilter),
        ('category', CategoryFilter),
        'tags',
        'transaction_type',
        'status',
        'source',
        'destination',
        'user',
    )

    list_editable = (
        'balanced',
    )
    search_fields = (
        'description',
    )
    date_hierarchy = 'datetime'

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())

    def get_queryset(self, request, *args, **kwargs):
        queryset = super().get_queryset(request, *args, **kwargs)
        if not request.user.is_superuser:
            queryset = queryset.filter(user=request.user)
        queryset = queryset.prefetch_related('tags', 'category', 'user',
                                             'source', 'destination')
        return queryset
