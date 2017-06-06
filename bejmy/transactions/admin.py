from django.contrib import admin

from bejmy.transactions.models import Transaction
from bejmy.transactions.forms import TransactionAdminForm


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    form = TransactionAdminForm
    list_display = (
        'description',
        'category',
        'amount',
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
