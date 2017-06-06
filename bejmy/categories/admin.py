from django.contrib import admin

from bejmy.categories.models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
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
