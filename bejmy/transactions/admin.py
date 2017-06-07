from django.contrib import admin

from mptt.admin import TreeRelatedFieldListFilter

from bejmy.transactions.models import Transaction
from bejmy.transactions.forms import TransactionAdminForm


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


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    form = TransactionAdminForm
    list_display_links = (
        'id',
        'amount',
    )
    list_display = (
        'id',
        'amount',
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

    fieldsets = (
        (None, {
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
        }),
        ('Info', {
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
        }),
    )

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())

    def get_form(self, request, *args, **kwargs):
        form = super().get_form(request, *args, **kwargs)
        form.user = request.user
        for field in ('source', 'destination', 'category'):
            form.base_fields[field].widget.can_add_related = False
            form.base_fields[field].widget.can_change_related = False
        return form

    def save_model(self, request, obj, *args, **kwargs):
        obj.modified_by = request.user
        if not obj.pk:
            obj.user = request.user
            obj.created_by = request.user
        return super().save_model(request, obj, *args, **kwargs)

    def get_queryset(self, request, *args, **kwargs):
        queryset = super().get_queryset(request, *args, **kwargs)
        if not request.user.is_superuser:
            queryset = queryset.filter(user=request.user)
        queryset = queryset.prefetch_related('tags', 'category', 'user',
                                             'source', 'destination')
        return queryset
