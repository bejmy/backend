from django.contrib import admin

from bejmy.categories.models import Category

from mptt.admin import MPTTModelAdmin


@admin.register(Category)
class CategoryAdmin(MPTTModelAdmin):
    list_display = (
        'name',
        'user',
        'transaction_type',
    )
    list_filter = (
        'user',
        'transaction_type',
    )
    search_fields = (
        'name',
    )
    raw_id_fields = ('parent',)

    def get_queryset(self, request, *args, **kwargs):
        queryset = super().get_queryset(request, *args, **kwargs)
        if not self.request.user.is_superuser():
            queryset = queryset.filter(user=request.user)
        return queryset
