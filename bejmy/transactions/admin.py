from django.contrib import admin

from bejmy.transactions.models import Transaction
from bejmy.transactions.forms import TransactionAdminForm


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
        'user',
        'transaction_type',
        'status',
        'source',
        'destination',
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
